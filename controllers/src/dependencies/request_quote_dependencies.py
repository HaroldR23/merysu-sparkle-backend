from adapters.src.services.EmailVerifierAdapter import EmailVerifierAdapter
from adapters.src.services.TurnstileCaptchaAdapter import TurnstileCaptchaAdapter
from use_cases.src.quote_request.use_case import QuoteRequestUseCase
from adapters.src.services.EmailSenderAdapter import EmailSenderAdapter

def get_quote_request_use_case():
    return QuoteRequestUseCase(
        email_sender=EmailSenderAdapter(),
        captcha_verifier=TurnstileCaptchaAdapter(),
        email_verifier=EmailVerifierAdapter()
    )
