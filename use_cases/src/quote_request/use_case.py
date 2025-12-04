from domain.src.exceptions.quote_request_exceptions import CaptchaValidationError, EmailSendingError, InvalidEmailError
from domain.src.ports.CaptchaService import CaptchaService
from domain.src.ports.EmailSenderService import EmailSenderService
from domain.src.ports.EmailVerifierService import EmailVerifierService

from settings.env_variables import COMPANY_EMAIL_RECIPIENT

from templates.get_admin_email_template import get_admin_email_template
from templates.get_customer_email_template import get_customer_email_template

from use_cases.src.quote_request.input import QuoteRequestInput

class QuoteRequestUseCase:
    def __init__(
            self, 
            email_sender: EmailSenderService,
            captcha_verifier: CaptchaService,
            email_verifier: EmailVerifierService
    ):
        self.email_sender = email_sender
        self.captcha_verifier = captcha_verifier
        self.email_verifier = email_verifier

    async def __call__(self, quote_request_input: QuoteRequestInput) -> tuple[bool, str]:

        captcha_validation = await self.captcha_verifier.verify(quote_request_input.captcha_token)

        if not captcha_validation["success"]:
            raise CaptchaValidationError()

        email_is_valid = await self.email_verifier.verify_email(quote_request_input.customer_email)

        if not email_is_valid:
            raise InvalidEmailError()

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
        except EmailSendingError as e:
            raise e

        return True, "Quote request processed and emails sent successfully."
