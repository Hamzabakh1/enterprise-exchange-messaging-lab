"""Offline Exchange routing model. This does not send or deliver email."""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


class ConfigurationError(ValueError):
    pass


def analyze(config: dict, sender: str, recipient: str, today: date) -> dict:
    """Return deterministic diagnostics for a synthetic message route."""
    required = {"accepted_domains", "connectors", "mailboxes", "certificate", "queue", "services", "databases", "dag"}
    if not required <= config.keys():
        raise ConfigurationError(f"Missing sections: {sorted(required - config.keys())}")
    if "@" not in sender or "@" not in recipient:
        raise ConfigurationError("Sender and recipient must be email addresses")
    domains = set(config["accepted_domains"])
    recipient_domain = recipient.rsplit("@", 1)[1].lower()
    sender_domain = sender.rsplit("@", 1)[1].lower()
    findings = []
    if sender_domain not in domains:
        findings.append("SENDER_DOMAIN_NOT_ACCEPTED")
    mailbox = config["mailboxes"].get(sender.lower())
    if mailbox is None:
        findings.append("SENDER_MAILBOX_NOT_FOUND")
    else:
        if mailbox["used_mb"] >= mailbox["send_quota_mb"]:
            findings.append("SEND_QUOTA_EXCEEDED")
    if config["queue"]["status"] != "Ready":
        findings.append("QUEUE_NOT_READY")
    if config["services"].get("MSExchangeTransport") != "Running":
        findings.append("TRANSPORT_SERVICE_DOWN")
    if config["services"].get("MSExchangeIS") != "Running":
        findings.append("INFORMATION_STORE_DOWN")
    if not any(db.get("mounted") for db in config["databases"].values()):
        findings.append("NO_MOUNTED_DATABASE")
    if config["dag"].get("enabled"):
        if len(config["dag"].get("members", [])) < 2:
            findings.append("DAG_TOO_FEW_MEMBERS")
        if not all(db.get("copy_status") == "Healthy" for db in config["databases"].values()):
            findings.append("DAG_COPY_UNHEALTHY")
    route_type = "internal" if recipient_domain in domains else "external"
    if route_type == "external":
        enabled = [c for c in config["connectors"] if c.get("enabled") and (recipient_domain in c.get("domains", []) or "*" in c.get("domains", []))]
        if not enabled:
            findings.append("NO_SEND_CONNECTOR")
        if config["certificate"].get("tls_required"):
            try:
                expiry = date.fromisoformat(config["certificate"]["expires"])
            except (KeyError, ValueError) as exc:
                raise ConfigurationError("Invalid certificate expiry") from exc
            if expiry < today:
                findings.append("TLS_CERTIFICATE_EXPIRED")
    if route_type == "internal" and recipient.lower() not in config["mailboxes"]:
        findings.append("RECIPIENT_MAILBOX_NOT_FOUND")
    return {"sender": sender, "recipient": recipient, "route_type": route_type,
            "findings": findings, "model_result": "CHECK_REQUIRED" if findings else "CONFIGURATION_APPEARS_VALID",
            "evidence_type": "SIMULATED_CONFIG_ANALYSIS"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--sender", required=True)
    parser.add_argument("--recipient", required=True)
    parser.add_argument("--date", type=date.fromisoformat, default=date.today())
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    print(json.dumps(analyze(config, args.sender, args.recipient, args.date), indent=2))


if __name__ == "__main__":
    main()
