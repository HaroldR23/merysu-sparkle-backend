from fastapi import APIRouter, Depends, Request

from slowapi import Limiter
from slowapi.util import get_remote_address

from use_cases.src.quote_request.input import QuoteRequestInput
from controllers.src.dependencies.request_quote_dependencies import get_quote_request_use_case
from controllers.src.dtos.quote_request import QuoteRequestDTO


quote_request_router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@quote_request_router.post("/quote-request")
@limiter.limit("5/minute")
async def get_quote_request(request: Request, requeste_quote: QuoteRequestDTO, quote_request_use_case=Depends(get_quote_request_use_case)):
    sent, message = await quote_request_use_case(quote_request_input=QuoteRequestInput(
        customer_name=requeste_quote.name,
        customer_email=requeste_quote.email,
        service_details=requeste_quote.service,
        customer_message=requeste_quote.message,
        captcha_token=requeste_quote.captcha_token
    ))

    return {"sent": sent, "message": message}
