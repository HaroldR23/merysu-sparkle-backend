import asyncio
import resend

from domain.src.exceptions.quote_request_exceptions import EmailSendingError
from domain.src.ports.EmailSenderService import EmailSenderService
from settings.env_variables import RESEND_API_KEY, COMPANY_EMAIL_SENDER

resend.api_key = RESEND_API_KEY
company_email_sender = COMPANY_EMAIL_SENDER

class EmailSenderAdapter(EmailSenderService):

    def _validate(self, response) -> None:
        if response.get("error"):
            error = response["error"].get("message", "Unknown error")
            raise EmailSendingError(f"Email sending failed: {error}")
        

    async def send_email(self, recipient: str, subject: str, body: str) -> None:
        payload: resend.Emails.SendParams = {
            "from": company_email_sender,
            "to": recipient,
            "subject": subject,
            "html": body,
        }

        def blocking_call():
            return resend.Emails.send(payload)
        
        response = await asyncio.to_thread(blocking_call)
        self._validate(response)

