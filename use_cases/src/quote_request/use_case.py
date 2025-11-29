from domain.src.ports.EmailSenderService import EmailSenderService
from settings.env_variables import COMPANY_EMAIL_RECIPIENT
from templates.get_admin_email_template import get_admin_email_template
from templates.get_customer_email_template import get_customer_email_template
from use_cases.src.quote_request.input import QuoteRequestInput

class QuoteRequestUseCase:
    def __init__(self, email_sender: EmailSenderService):
        self.email_sender = email_sender

    async def __call__(self, quote_request_input: QuoteRequestInput) -> tuple[bool, str]:
        admin_email_body = get_admin_email_template(
            customer_name=quote_request_input.customer_name,
            customer_email=quote_request_input.customer_email,
            service_details=quote_request_input.service_details,
            customer_message=quote_request_input.customer_message
        )

        customer_email_body = get_customer_email_template(
            customer_name=quote_request_input.customer_name
        )

        try:
            await self.email_sender.send_email(
                body=admin_email_body,
                recipient=COMPANY_EMAIL_RECIPIENT,
                subject="New Quote Request Received"
            )

            await self.email_sender.send_email(
                body=customer_email_body,
                recipient=quote_request_input.customer_email,
                subject="Thank You for Your Quote Request"
            )
        except Exception as e:
            return False, f"Failed to send emails: {str(e)}"

        return True, "Quote request processed and emails sent successfully."
