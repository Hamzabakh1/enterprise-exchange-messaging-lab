# Validation report — 2026-10-21

Local execution: Windows x64, bundled Python 3.12.14, PowerShell 7.6.5. No Exchange Server or mailbox was connected.

| Test | Expected | Actual | Environment | Timestamp UTC | Evidence | Status |
|---|---|---|---|---|---|---|
| Synthetic route unit suite | 6 pass | 6 pass, exit 0 | Local Python | 2026-10-21 06:01 | [unittest.txt](tests/evidence/unittest.txt) | PASS |
| PowerShell parser | 0 errors | 0 errors in 1 file | Local PowerShell | 2026-10-21 05:28 | [parser.txt](tests/evidence/parser.txt) | PASS |
| Example route | Explicit simulated marker | `SIMULATED_CONFIG_ANALYSIS`, no findings | Local Python | 2026-10-21 06:02 | [route.json](tests/evidence/route.json) | PASS |
| Exchange installation/mail delivery/DAG | Real server result | Not executed | Server/license/capacity unavailable | N/A | [audit](ENVIRONMENT_AUDIT.md) | BLOCKED |
| Eight incident drills | Fault and recovery evidence | Not executed | Exchange lab unavailable | N/A | [runbooks](TROUBLESHOOTING.md) | BLOCKED |

`CONFIGURATION_APPEARS_VALID` means the tiny synthetic model found no configured fault. It does not mean SMTP delivery occurred. The server quality gates and target score remain open.
