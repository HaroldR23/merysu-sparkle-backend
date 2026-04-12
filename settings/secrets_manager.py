import boto3
import json
import time
from typing import Dict, Optional


class SecretsManager:

  def __init__(self, secret_name: str = 'prod/merysu-backend', region: str = 'us-east-1'):
    self.secret_name = secret_name
    self.region = region
    self.client = boto3.client('secretsmanager', region_name=region)
    self._secrets_cache: Optional[Dict] = None
    self._cache_timestamp: float = 0
    self.cache_ttl = 300  # 5 minutos


  def _fetch_secrets_from_aws(self) -> Dict:
    """Obtiene secretos frescos desde AWS Secrets Manager"""
    try:
        response = self.client.get_secret_value(SecretId=self.secret_name)
        secrets = json.loads(response['SecretString'])
        print(f"Secretos obtenidos desde AWS Secrets Manager")
        return secrets

    except Exception as e:
        print(f"Error obteniendo secretos: {e}")
        raise e


  def get_secrets(self) -> Dict:
    """Obtiene secretos con caché automático"""
    current_time = time.time()

    # Verificar si el caché es válido
    if (self._secrets_cache and 
        (current_time - self._cache_timestamp) < self.cache_ttl):
        return self._secrets_cache
    # Obtener secretos frescos y actualizar caché
    self._secrets_cache = self._fetch_secrets_from_aws()
    self._cache_timestamp = current_time
    return self._secrets_cache


  def get_secret(self, key: str) -> str:
    """Obtiene un secreto específico por clave"""
    secrets = self.get_secrets()

    if key not in secrets:
      raise KeyError(f"Secreto '{key}' no encontrado")

    return secrets[key]


# Instancia global del gestor de secretos

secrets_manager = SecretsManager()
