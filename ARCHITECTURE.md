# Exchange SE architecture

**DOCUMENTED ONLY.** EX01 at 192.0.2.50 is the proposed Mailbox server; EX02 at .51 is optional for DAG evaluation. Both join `corp.example.test` and query DC01/DC02 for directory services. MX records, public DNS, a verified SMTP namespace, public certificate and Internet routing are intentionally absent from the local lab. A real design must provide those dependencies, relay policy and anti-spam controls.

Messages enter a scoped Receive Connector, pass through transport/categorization, then route to a local mailbox database or Send Connector. Queue state, message tracking events and protocol logs provide separate evidence. An optional DAG requires witness placement, quorum, database copies and client access/load balancing; a single EX01 is not HA. Cloud hybrid adds an Exchange Online trust and accepted-domain/connector boundary, with identity synchronization handled by project 3.

Exchange SE support must be rechecked at deployment time. Microsoft states Exchange 2016/2019 support ended October 2025; they are not recommended for new installation. [Editable flow](assets/diagrams/messaging-flow.mmd).
