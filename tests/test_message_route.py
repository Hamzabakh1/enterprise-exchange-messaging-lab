import copy
import importlib.util
import json
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("message_route", ROOT / "scripts/automation/message_route.py")
route = importlib.util.module_from_spec(spec)
spec.loader.exec_module(route)
BASE = json.loads((ROOT / "examples/synthetic-data/topology.json").read_text(encoding="utf-8"))


class RouteTests(unittest.TestCase):
    def test_healthy_model_is_explicitly_simulated(self):
        result = route.analyze(BASE, "lab.alice@atlas.example.test", "external@example.org", date(2026, 10, 21))
        self.assertEqual(result["model_result"], "CONFIGURATION_APPEARS_VALID")
        self.assertEqual(result["evidence_type"], "SIMULATED_CONFIG_ANALYSIS")

    def test_quota_failure(self):
        config = copy.deepcopy(BASE)
        config["mailboxes"]["lab.alice@atlas.example.test"]["used_mb"] = 1024
        self.assertIn("SEND_QUOTA_EXCEEDED", route.analyze(config, "lab.alice@atlas.example.test", "external@example.org", date(2026, 10, 21))["findings"])

    def test_queue_and_certificate_failure(self):
        config = copy.deepcopy(BASE)
        config["queue"]["status"] = "Retry"
        config["certificate"]["expires"] = "2025-01-01"
        findings = route.analyze(config, "lab.alice@atlas.example.test", "external@example.org", date(2026, 10, 21))["findings"]
        self.assertIn("QUEUE_NOT_READY", findings)
        self.assertIn("TLS_CERTIFICATE_EXPIRED", findings)

    def test_missing_connector(self):
        config = copy.deepcopy(BASE)
        config["connectors"] = []
        self.assertIn("NO_SEND_CONNECTOR", route.analyze(config, "lab.alice@atlas.example.test", "external@example.org", date(2026, 10, 21))["findings"])

    def test_service_and_database_outage(self):
        config = copy.deepcopy(BASE)
        config["services"]["MSExchangeTransport"] = "Stopped"
        config["databases"]["DB01"]["mounted"] = False
        findings = route.analyze(config, "lab.alice@atlas.example.test", "lab.bob@atlas.example.test", date(2026, 10, 21))["findings"]
        self.assertIn("TRANSPORT_SERVICE_DOWN", findings)
        self.assertIn("NO_MOUNTED_DATABASE", findings)

    def test_dag_copy_and_member_risk(self):
        config = copy.deepcopy(BASE)
        config["dag"] = {"enabled": True, "members": ["EX01"]}
        config["databases"]["DB01"]["copy_status"] = "Failed"
        findings = route.analyze(config, "lab.alice@atlas.example.test", "lab.bob@atlas.example.test", date(2026, 10, 21))["findings"]
        self.assertIn("DAG_TOO_FEW_MEMBERS", findings)
        self.assertIn("DAG_COPY_UNHEALTHY", findings)


if __name__ == "__main__":
    unittest.main()
