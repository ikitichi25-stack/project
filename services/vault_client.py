"""
Vault secrets client for SecureShop microservices
Usage:
    from vault_client import VaultClient
    
    client = VaultClient()
    jwt_secret = client.get_secret('jwt', 'secret')
    db_password = client.get_secret('database', 'password')
"""

import os
import requests
from typing import Dict, Optional


class VaultClient:
    def __init__(
        self,
        vault_addr: Optional[str] = None,
        vault_token: Optional[str] = None,
        mount_path: str = "secrets"
    ):
        self.vault_addr = vault_addr or os.getenv("VAULT_ADDR", "http://vault:8200")
        self.vault_token = vault_token or os.getenv("VAULT_TOKEN", "dev-token-local")
        self.mount_path = mount_path
        self.base_path = f"{self.vault_addr}/v1/{mount_path}"
        self.headers = {
            "X-Vault-Token": self.vault_token,
            "Content-Type": "application/json"
        }

    def get_secret(self, secret_path: str, key: Optional[str] = None) -> any:
        """
        Fetch a secret from Vault
        
        Args:
            secret_path: Path to secret (e.g., 'secureshop/jwt')
            key: Optional key within the secret (e.g., 'secret')
        
        Returns:
            The secret value or entire secret dict if key is None
        
        Example:
            jwt_secret = client.get_secret('secureshop/jwt', 'secret')
            all_jwt_secrets = client.get_secret('secureshop/jwt')
        """
        try:
            url = f"{self.base_path}/data/{secret_path}"
            response = requests.get(url, headers=self.headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                secret_data = data.get("data", {}).get("data", {})
                
                if key:
                    return secret_data.get(key)
                return secret_data
            elif response.status_code == 404:
                raise ValueError(f"Secret not found: {secret_path}")
            else:
                raise Exception(f"Vault error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Failed to fetch secret from Vault: {e}")
            # Fallback to environment variables in development
            return os.getenv(f"{secret_path.upper()}_{key.upper()}")

    def list_secrets(self, secret_path: str) -> list:
        """List all secrets under a path"""
        try:
            url = f"{self.base_path}/metadata/{secret_path}"
            response = requests.request('LIST', url, headers=self.headers, timeout=5)
            
            if response.status_code == 200:
                return response.json().get("data", {}).get("keys", [])
            return []
        except Exception as e:
            print(f"Failed to list secrets: {e}")
            return []


if __name__ == "__main__":
    # Test the Vault client
    client = VaultClient()
    
    print("Testing Vault connectivity...")
    try:
        jwt_creds = client.get_secret("secureshop/jwt")
        print(f"JWT credentials: {jwt_creds}")
    except Exception as e:
        print(f"Error: {e}")
