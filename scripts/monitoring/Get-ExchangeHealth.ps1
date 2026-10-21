# Read-only example for an approved Exchange Server SE Management Shell session.
[CmdletBinding()]
param([Parameter(Mandatory)][string]$ExpectedServer)
$ErrorActionPreference = 'Stop'
if (-not (Get-Command Get-ExchangeServer -ErrorAction SilentlyContinue)) { throw 'Exchange Management Shell is not connected.' }
$server = Get-ExchangeServer -Identity $ExpectedServer
if (-not $server) { throw 'Expected server not found.' }
[pscustomobject]@{
    Server = $server.Name
    ServerHealth = @(Get-ServerHealth -Identity $ExpectedServer | Where-Object AlertValue -ne Healthy | Select-Object Name,AlertValue)
    Queues = @(Get-Queue -Server $ExpectedServer | Select-Object Identity,Status,MessageCount)
    Certificate = @(Get-ExchangeCertificate -Server $ExpectedServer | Select-Object Thumbprint,NotAfter,Services,Status)
    CollectedUtc = [DateTime]::UtcNow.ToString('o')
}
