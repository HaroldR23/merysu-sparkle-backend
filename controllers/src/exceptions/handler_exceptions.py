from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from http import HTTPStatus


from starlette.exceptions import HTTPException

from domain.src.exceptions.quote_request_exceptions import CaptchaValidationError, EmailSendingError, InvalidEmailError

def register_exception_handler(app: FastAPI) -> None:

    @app.exception_handler(CaptchaValidationError)
    def captcha_error_handler(request: Request, exc: CaptchaValidationError):
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content={"detail": exc.message},
        )

    @app.exception_handler(EmailSendingError)
    def email_sending_error_handler(request: Request, exc: EmailSendingError):
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"detail": exc.message},
        )
    
    @app.exception_handler(InvalidEmailError)
    def invalid_email_error_handler(request: Request, exc: InvalidEmailError):
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content={"detail": exc.message},
        )
