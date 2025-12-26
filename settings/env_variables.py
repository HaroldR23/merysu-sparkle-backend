from dotenv import load_dotenv
import os

load_dotenv()

COMPANY_EMAIL_SENDER = os.environ.get("COMPANY_EMAIL_SENDER", "asasd@example.com")
COMPANY_EMAIL_RECIPIENT = os.environ.get("COMPANY_EMAIL_RECIPIENT", "default_recipient@example.com")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "default_api_key")
TURNSTILE_SECRET_KEY = os.environ.get("TURNSTILE_SECRET_KEY", "default_turnstile_key")

def get_allowed_origins() -> list[str]:
    origins = os.environ.get("CORS_ALLOWED_ORIGINS", "")
    return [origin.strip() for origin in origins.split(",") if origin.strip()]
