# SecureShop Deliverables

This document tracks the project deliverables for the SecureShop DevSecOps repository.

## D1 - Threat Model
- Provided in `THREAT_MODEL.md`
- Contains system overview, threat model, and STRIDE worksheet.

## D2 - Working microservices application
- Docker Compose application defined in `docker-compose.yml`
- Service implementations in `services/*`
- API gateway in `api-gateway/`

## D3 - CI/CD pipeline
- Implemented in `.github/workflows/ci.yml`
- Scans include SAST, SCA, secret scanning, container scanning, IaC scanning, and DAST.

## D4 - Tool findings summary
- Findings placeholders in `SECURITY_FINDINGS.md`
- Pipeline generates reports from Bandit, Semgrep, pip-audit, npm audit, Trivy, Checkov, and OWASP ZAP.

## D5 - Security report template
- Provided in `SECURITY_REPORT.md`
- Also exported as `SECURITY_REPORT.pdf`
- Can be extended into a full report for executive review.

## D6 - Live demo support
- Local deployment via Docker Compose
- DAST helper script in `scripts/run_dast.sh`
- IaC scan helper in `scripts/scan_iac.sh`
