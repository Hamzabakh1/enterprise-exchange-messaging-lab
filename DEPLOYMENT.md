# Exchange SE deployment path

**DOCUMENTED ONLY; do not run on the current host.**

1. Recheck supportability matrix, current CU/SU and sizing. Obtain license/media and a separate isolated test forest with healthy DNS, replication and time.
2. Prepare AD schema and organization per the exact current Exchange SE setup guide; record setup build and prerequisites. Changes affect the whole forest and need a restore plan.
3. Install EX01 on a supported Windows Server, review setup logs and post-install health. Configure internal/external URLs, certificate and minimum required Receive/Send Connectors.
4. Create synthetic mailbox/database, send internal test messages, inspect tracking and queues, then test external routing only with a domain and route owned by the operator.
5. If enough resources exist, add EX02, witness and DAG, then test copy health, switchover, failover and restore separately. Capture real evidence at each step.

Current status: none of these server steps has been executed. Use [configuration modules](docs/configuration/CONFIGURATION.md) for the verification matrix.
