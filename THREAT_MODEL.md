# SecureShop Threat Model

## System Overview

SecureShop is a microservices-based e-commerce platform with six services behind an Nginx API gateway.

- User Service: authentication, registration, JWT issuance
- Product Service: catalogue and search
- Order Service: cart and checkout
- Payment Service: payment processing stub
- Notification Service: email/SMS dispatch
- Inventory Service: stock reservation and release

## Data Flow Diagram (DFD)

1. External client -> API gateway -> User/Product/Order/Payment/Inventory services
2. User Service issues JWT tokens
3. Order Service queries Product and Inventory services and posts to Notification service
4. Payment Service accepts payment requests

## STRIDE Analysis

- Spoofing
  - Risk: invalid JWT tokens, weak authentication endpoints
  - Mitigation: verify JWT signature and expiration, enforce strong credentials

- Tampering
  - Risk: manipulated service requests, unauthorized order updates
  - Mitigation: validate input, enforce authorization checks, use HTTPS in production

- Repudiation
  - Risk: missing audit trail for orders and payments
  - Mitigation: log user actions, store request metadata, add trace IDs if needed

- Information Disclosure
  - Risk: leaked secrets in source code or environment files
  - Mitigation: do not commit secrets, use `.env` for runtime values, scan with Gitleaks

- Denial of Service
  - Risk: excessive API requests or expensive search queries
  - Mitigation: use rate limiting at API gateway, set request limits

- Elevation of Privilege
  - Risk: unauthorized access to admin operations or order approval flow
  - Mitigation: enforce JWT claims and role checks, isolate services by function
