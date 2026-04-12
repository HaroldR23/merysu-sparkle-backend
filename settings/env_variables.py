from dotenv import load_dotenv
import os

from settings.secrets_manager import secrets_manager

load_dotenv()

ENV = os.environ.get("ENV", "development")
COMPANY_EMAIL_SENDER = os.environ.get("COMPANY_EMAIL_SENDER", "asasd@example.com")
COMPANY_EMAIL_RECIPIENT = os.environ.get("COMPANY_EMAIL_RECIPIENT", "default_recipient@example.com")

if ENV == "production":
    print("Cargando variables de entorno desde AWS Secrets Manager")
    RESEND_API_KEY = secrets_manager.get_secret('RESEND_API_KEY')
    TURNSTILE_SECRET_KEY = secrets_manager.get_secret('TURNSTILE_SECRET_KEY')
    DATABASE_URL = secrets_manager.get_secret('DATABASE_URL')

else:
    RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
    TURNSTILE_SECRET_KEY = os.environ.get("TURNSTILE_SECRET_KEY", "")
    DATABASE_URL = os.environ.get("DATABASE_URL", "")

def get_allowed_origins() -> list[str]:
    origins = os.environ.get("CORS_ALLOWED_ORIGINS", "")
    return [origin.strip() for origin in origins.split(",") if origin.strip()]
