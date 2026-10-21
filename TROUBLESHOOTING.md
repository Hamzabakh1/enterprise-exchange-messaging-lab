# Exchange failure runbooks

**Status: DOCUMENTED ONLY.** Execute fault injection only in an isolated, adequately sized Exchange SE lab. For each case record pre-state, synthetic test message ID, impact, timestamps, diagnostic output, root cause, correction, post-state and monitoring.

## 1. User cannot send
**Business impact:** Outbound business mail delayed. **Diagnostic workflow / PowerShell:** Get-MessageTrackingLog, Get-Queue, mailbox send quota, client submission and send connector. **Likely root cause to reproduce:** Quota, connector or transport issue. **Recovery:** Correct the observed constraint; avoid queue deletion. **Validation:** Accepted SEND and DELIVER/SEND tracking events; external receipt if owned. **Monitoring:** correlate health, queue length, tracking logs and certificate/database state; alert on sustained abnormality.

## 2. User cannot receive
**Business impact:** Inbound mail delayed or bounced. **Diagnostic workflow / PowerShell:** MX, accepted domain, receive connector, protocol log, recipient and tracking. **Likely root cause to reproduce:** DNS, connector scope or recipient resolution. **Recovery:** Restore approved DNS/connector/recipient configuration. **Validation:** SMTP acceptance and mailbox delivery are both evidenced. **Monitoring:** correlate health, queue length, tracking logs and certificate/database state; alert on sustained abnormality.

## 3. Quota exceeded
**Business impact:** Mail flow blocked for one mailbox. **Diagnostic workflow / PowerShell:** Get-MailboxStatistics and Get-Mailbox quota settings. **Likely root cause to reproduce:** ProhibitSend threshold reached. **Recovery:** Apply approved quota adjustment or archive/cleanup. **Validation:** New test message succeeds and mailbox usage is below limit. **Monitoring:** correlate health, queue length, tracking logs and certificate/database state; alert on sustained abnormality.

## 4. Queue stops processing
**Business impact:** Multiple messages delayed. **Diagnostic workflow / PowerShell:** Get-Queue, Get-Message, transport service and event logs. **Likely root cause to reproduce:** Next hop, DNS, service or disk issue. **Recovery:** Repair root cause then resume/retry queue as appropriate. **Validation:** Queue drains and tracking shows delivery. **Monitoring:** correlate health, queue length, tracking logs and certificate/database state; alert on sustained abnormality.

## 5. TLS certificate fails
**Business impact:** Secure route rejects connection. **Diagnostic workflow / PowerShell:** Get-ExchangeCertificate, connector FQDN, protocol log, chain and date. **Likely root cause to reproduce:** Expired/wrong name/unbound certificate. **Recovery:** Install approved valid certificate and bind service. **Validation:** TLS negotiation and mail flow succeed. **Monitoring:** correlate health, queue length, tracking logs and certificate/database state; alert on sustained abnormality.

## 6. Exchange service unavailable
**Business impact:** Client or transport outage. **Diagnostic workflow / PowerShell:** Get-ServerHealth, Get-Service, events, dependencies. **Likely root cause to reproduce:** Service crash or resource exhaustion. **Recovery:** Restore dependency/service, investigate crash. **Validation:** Service healthy and functional mail test. **Monitoring:** correlate health, queue length, tracking logs and certificate/database state; alert on sustained abnormality.

## 7. Mailbox database fails
**Business impact:** Affected mailboxes unavailable. **Diagnostic workflow / PowerShell:** Get-MailboxDatabaseCopyStatus, logs, storage, event logs. **Likely root cause to reproduce:** Disk, copy or log fault. **Recovery:** Activate healthy copy or restore backup per plan. **Validation:** Database mounted and mailbox test passes. **Monitoring:** correlate health, queue length, tracking logs and certificate/database state; alert on sustained abnormality.

## 8. DAG evaluation
**Business impact:** HA claim at risk. **Diagnostic workflow / PowerShell:** Get-DatabaseAvailabilityGroup, copy status, witness/quorum, controlled switchover. **Likely root cause to reproduce:** Quorum or unhealthy copy. **Recovery:** Repair quorum/copy before failover test. **Validation:** Measured failover and client continuity with evidence. **Monitoring:** correlate health, queue length, tracking logs and certificate/database state; alert on sustained abnormality.
