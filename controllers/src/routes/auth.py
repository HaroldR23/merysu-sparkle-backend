from fastapi import APIRouter, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from controllers.src.dependencies.auth_dependencies import get_auth_login_use_case
from controllers.src.dtos.auth import LoginRequestDTO, LoginResponseDTO, UserInfoDTO
from use_cases.src.auth_login.input import AuthLoginInput
from use_cases.src.auth_login.use_case import AuthLoginUseCase

auth_router = APIRouter(prefix="/auth")
limiter = Limiter(key_func=get_remote_address)


@auth_router.post("/login", response_model=LoginResponseDTO)
@limiter.limit("10/minute")
async def login(
    request: Request,
    login_dto: LoginRequestDTO,
    auth_login_use_case: AuthLoginUseCase = Depends(get_auth_login_use_case),
):
    result = auth_login_use_case(
        auth_login_input=AuthLoginInput(
            email=login_dto.email,
            password=login_dto.password,
        )
    )

    return LoginResponseDTO(
        access_token=result.access_token,
        user=UserInfoDTO(
            id=str(result.user_id),
            name=result.name,
            role=result.role,
        ),
    )
