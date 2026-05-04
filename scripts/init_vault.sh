#!/bin/bash
set -e

echo "Initializing HashiCorp Vault with SecureShop secrets..."

# Wait for Vault to be ready
echo "Waiting for Vault to be ready..."
sleep 5

# Export Vault address and token
export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_TOKEN=dev-token-local

echo "Testing Vault connection..."
vault status || exit 1

# Enable kv-v2 secrets engine at /secrets
echo "Enabling kv-v2 secrets engine..."
vault secrets enable -version=2 -path=secrets kv || echo "Already enabled"

# Store JWT secret
echo "Storing JWT_SECRET..."
vault kv put secrets/secureshop/jwt \
  secret="your-super-secret-jwt-key-change-in-production" \
  issuer="secureshop" \
  expiry="3600"

# Store database credentials
echo "Storing database credentials..."
vault kv put secrets/secureshop/database \
  username="secureshop_user" \
  password="change-me-in-production" \
  host="localhost" \
  port="5432" \
  database="secureshop_db"

# Store payment API keys
echo "Storing payment service credentials..."
vault kv put secrets/secureshop/payment \
  api_key="pk_test_change_me_in_production" \
  api_secret="sk_test_change_me_in_production" \
  provider="stripe"

# Store SMTP credentials for notifications
echo "Storing SMTP credentials..."
vault kv put secrets/secureshop/smtp \
  host="smtp.gmail.com" \
  port="587" \
  username="noreply@secureshop.local" \
  password="change-me-in-production"

# Store RabbitMQ credentials
echo "Storing RabbitMQ credentials..."
vault kv put secrets/secureshop/rabbitmq \
  username="guest" \
  password="guest" \
  host="rabbitmq" \
  port="5672"

# List all stored secrets
echo ""
echo "Vault secrets initialized successfully!"
echo ""
echo "Available secrets paths:"
vault kv list secrets/secureshop/

echo ""
echo "To read secrets in your application:"
echo "  export VAULT_ADDR=http://vault:8200"
echo "  export VAULT_TOKEN=dev-token-local"
echo "  vault kv get secrets/secureshop/jwt"
