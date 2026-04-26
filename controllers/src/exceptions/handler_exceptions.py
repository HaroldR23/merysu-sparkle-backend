from slowapi.errors import RateLimitExceeded

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from http import HTTPStatus

from domain.src.exceptions.auth_exceptions import InvalidCredentialsError
from domain.src.exceptions.customer_exceptions import CustomerCreationError, CustomerNotFoundError, InvalidCustomerDataError
from domain.src.exceptions.employee_exceptions import EmployeeCreationError, EmployeeNotFoundError, InvalidEmployeeDataError
from domain.src.exceptions.quote_request_exceptions import CaptchaValidationError, EmailSendingError, InvalidEmailError
from domain.src.exceptions.service_exceptions import InvalidServiceDataError, ServiceCreationError

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

    @app.exception_handler(InvalidEmployeeDataError)
    def invalid_employee_data_handler(request: Request, exc: InvalidEmployeeDataError):
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content={"detail": exc.message},
        )

    @app.exception_handler(EmployeeCreationError)
    def employee_creation_error_handler(request: Request, exc: EmployeeCreationError):
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"detail": exc.message},
        )

    @app.exception_handler(EmployeeNotFoundError)
    def employee_not_found_handler(request: Request, exc: EmployeeNotFoundError):
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={"detail": exc.message},
        )

    @app.exception_handler(InvalidCustomerDataError)
    def invalid_customer_data_handler(request: Request, exc: InvalidCustomerDataError):
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content={"detail": exc.message},
        )

    @app.exception_handler(CustomerCreationError)
    def customer_creation_error_handler(request: Request, exc: CustomerCreationError):
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"detail": exc.message},
        )

    @app.exception_handler(CustomerNotFoundError)
    def customer_not_found_handler(request: Request, exc: CustomerNotFoundError):
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={"detail": exc.message},
        )

    @app.exception_handler(InvalidServiceDataError)
    def invalid_service_data_handler(request: Request, exc: InvalidServiceDataError):
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content={"detail": exc.message},
        )

    @app.exception_handler(ServiceCreationError)
    def service_creation_error_handler(request: Request, exc: ServiceCreationError):
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"detail": exc.message},
        )

    @app.exception_handler(InvalidCredentialsError)
    def invalid_credentials_handler(request: Request, exc: InvalidCredentialsError):
        return JSONResponse(
            status_code=HTTPStatus.UNAUTHORIZED,
            content={"detail": exc.message},
        )

    @app.exception_handler(RateLimitExceeded)
    def rate_limit_handler(request: Request, exc: RateLimitExceeded):
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests, please wait."}
        )
