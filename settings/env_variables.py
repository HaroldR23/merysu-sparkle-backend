from dotenv import load_dotenv
import os

load_dotenv()

COMPANY_EMAIL_SENDER = os.environ.get("COMPANY_EMAIL_SENDER", "asasd@example.com")
COMPANY_EMAIL_RECIPIENT = os.environ.get("COMPANY_EMAIL_RECIPIENT", "default_recipient@example.com")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "default_api_key")
