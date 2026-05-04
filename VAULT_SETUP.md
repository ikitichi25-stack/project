# Vault Secrets Management for SecureShop

## Overview

Vault is included in the docker-compose setup in dev mode to manage and store runtime secrets. This prevents hardcoding sensitive information in code or environment variables.

## Architecture

- **Vault Server:** Runs in dev mode on port 8200
- **Dev Token:** `dev-token-local` (for development only; use proper auth in production)
- **Mount Path:** `/secrets/kv-v2`
- **Secrets Organization:** `secrets/secureshop/{service-name}`

## Starting Vault

Vault starts automatically with:
```bash
docker compose up
```

Access the Vault UI at: `http://localhost:8200/ui`
- Token: `dev-token-local`

## Initializing Secrets

After Vault is running, initialize all secrets:
```bash
bash scripts/init_vault.sh
```

This populates secrets for:
- JWT authentication
- Database credentials
- Payment API keys
- SMTP/Email configuration
- RabbitMQ message broker

## Using Vault in Python Services

### Option 1: Using VaultClient (Recommended)

```python
from services.vault_client import VaultClient

# Initialize client (auto-detects VAULT_ADDR and VAULT_TOKEN from env)
client = VaultClient()

# Get a specific secret
jwt_secret = client.get_secret('secureshop/jwt', 'secret')
db_password = client.get_secret('secureshop/database', 'password')

# Get entire secret object
all_jwt_secrets = client.get_secret('secureshop/jwt')
```

### Option 2: Direct HTTP Requests

```python
import requests

VAULT_ADDR = 'http://vault:8200'
VAULT_TOKEN = 'dev-token-local'
headers = {'X-Vault-Token': VAULT_TOKEN}

response = requests.get(
    f'{VAULT_ADDR}/v1/secrets/data/secureshop/jwt',
    headers=headers
)
secret = response.json()['data']['data']
jwt_secret = secret['secret']
```

## Available Secrets

| Path | Keys | Purpose |
| --- | --- | --- |
| `secureshop/jwt` | secret, issuer, expiry | JWT token signing |
| `secureshop/database` | username, password, host, port, database | Database access |
| `secureshop/payment` | api_key, api_secret, provider | Payment processor integration |
| `secureshop/smtp` | host, port, username, password | Email notifications |
| `secureshop/rabbitmq` | username, password, host, port | Message broker |

## Security Considerations

### Development (Current Setup)
- Dev token and in-memory storage
- Suitable for local testing
- No persistence

### Production Deployment
1. **Use proper authentication:**
   - JWT auth
   - Kubernetes auth
   - AWS IAM/AppRole
   - LDAP/OAuth

2. **Storage backend:**
   - Consul backend (distributed)
   - PostgreSQL backend (encrypted)
   - Vault Enterprise Replication

3. **Encryption:**
   - Enable Vault auto-unseal
   - Use encryption-at-rest
   - Implement TLS for all communication

4. **Access controls:**
   - Implement least-privilege policies
   - Use separate tokens per service
   - Enable audit logging

## Troubleshooting

**Issue:** Vault connection refused
```bash
# Check Vault is running
docker compose logs vault

# Restart Vault
docker compose restart vault
```

**Issue:** Secrets not initialized
```bash
# Run init script
bash scripts/init_vault.sh

# Verify secrets
vault kv list secrets/secureshop/
```

**Issue:** Permission denied accessing secrets
```bash
# Check token is valid
vault token lookup

# Renew token if needed
vault token renew
```

## References

- [Vault Documentation](https://www.vaultproject.io/docs)
- [Vault Dev Mode](https://www.vaultproject.io/docs/concepts/dev-server)
- [Vault Policies](https://www.vaultproject.io/docs/concepts/policies)
