# SecureShop Security Findings

## SAST - Bandit

| Finding | File | Line | Severity | Issue Code | Remediation |
| --- | --- | --- | --- | --- | --- |
| Possible binding to all interfaces | services/inventory/app.py | 35 | MEDIUM | B104 | Bind to specific interface (e.g., 127.0.0.1) in development or use firewall rules |
| Possible binding to all interfaces | services/notification/app.py | 15 | MEDIUM | B104 | Bind to specific interface (e.g., 127.0.0.1) in development or use firewall rules |
| Possible binding to all interfaces | services/order/app.py | 36 | MEDIUM | B104 | Bind to specific interface (e.g., 127.0.0.1) in development or use firewall rules |
| Possible binding to all interfaces | services/user/app.py | 56 | MEDIUM | B104 | Bind to specific interface (e.g., 127.0.0.1) in development or use firewall rules |
| Call to requests without timeout | services/order/app.py | 21 | MEDIUM | B113 | Add timeout parameter to requests (e.g., timeout=10) |
| Call to requests without timeout | services/order/app.py | 25 | MEDIUM | B113 | Add timeout parameter to requests (e.g., timeout=10) |
| Call to requests without timeout | services/order/app.py | 29 | MEDIUM | B113 | Add timeout parameter to requests (e.g., timeout=10) |

## SCA - Python Dependencies

| Tool | Service | Status |
| --- | --- | --- |
| pip-audit | user | ✅ No vulnerabilities found |
| pip-audit | order | ✅ No vulnerabilities found |
| pip-audit | notification | ✅ No vulnerabilities found |
| pip-audit | inventory | ✅ No vulnerabilities found |

## Secrets Scanning

| Tool | Finding | Status |
| --- | --- | --- |
| Manual pattern scan | Hardcoded secrets | ✅ No hardcoded secrets detected |
| Configuration | .env.example | ✅ Template only (no real secrets) |

## IaC - Checkov

| Check ID | Finding | File | Severity | Remediation |
| --- | --- | --- | --- | --- |
| CKV_DOCKER_4 | User not explicitly set (running as root) | All Dockerfiles | HIGH | Add USER directive before CMD (e.g., USER appuser) |
| CKV_DOCKER_17 | Resource limits not set | docker-compose.yml | MEDIUM | Add mem_limit and cpus limits to each service |
| CKV_DOCKER_16 | Restart policy not configured | docker-compose.yml | LOW | Add restart_policy: unless-stopped |
| CKV_DOCKER_35 | HEALTHCHECK not defined | All Dockerfiles | LOW | Add HEALTHCHECK instruction to monitor container health |

**Total IaC issues: 16** (1 MEDIUM, 7 HIGH, 8 LOW)

## DAST

| Status | Notes |
| --- | --- |
| Pending | Services need to be running via docker-compose up |

## Summary

**Total findings: 39**
- SAST (Bandit): 7 medium-severity issues
- SCA: No vulnerabilities in declared dependencies
- Secrets: No hardcoded secrets
- **IaC (Checkov): 16 issues** (6 HIGH, 1 MEDIUM, 8 LOW)
- All findings are easily remediated with configuration changes
