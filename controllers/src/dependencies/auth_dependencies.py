from fastapi import Depends
from sqlalchemy.orm import Session

from adapters.src.repositories.sql_alchemy_repository.UserRepository import UserRepositoryAdapter
from adapters.src.repositories.sql_alchemy_repository.db_config import get_db
from adapters.src.services.JWTAdapter import JWTAdapter
from adapters.src.services.PasswordHasherAdapter import PasswordHasherAdapter
from use_cases.src.auth_login.use_case import AuthLoginUseCase


def get_auth_login_use_case(db: Session = Depends(get_db)) -> AuthLoginUseCase:
    return AuthLoginUseCase(
        user_repository=UserRepositoryAdapter(session=db),
        jwt_service=JWTAdapter(),
        password_hasher=PasswordHasherAdapter(),
    )
