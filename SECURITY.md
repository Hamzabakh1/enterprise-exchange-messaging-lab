# Security review

The local analyzer reads only synthetic JSON and has no network or Exchange connection. The monitoring sample performs read-only Exchange queries after verifying an expected server. In a live lab, prevent anonymous relay; restrict connector bindings and permissions, validate TLS names/expiry/trust, scope RBAC and mailbox delegation, patch the supported SE build, audit admin actions and protect backup copies. Keep credentials, certificates and real SMTP domains out of Git. Security implementation in Exchange itself is **BLOCKED** until a supported lab exists.
