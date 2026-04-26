from adapters.src.services.PasswordHasherAdapter import PasswordHasherAdapter
from domain.src.exceptions.auth_exceptions import InvalidCredentialsError
from domain.src.ports.repositories.UserRepository import UserRepository
from domain.src.ports.services.JWTService import JWTService
from use_cases.src.auth_login.input import AuthLoginInput
from use_cases.src.auth_login.output import AuthLoginOutput


class AuthLoginUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        jwt_service: JWTService,
        password_hasher: PasswordHasherAdapter,
    ):
        self.user_repository = user_repository
        self.jwt_service = jwt_service
        self.password_hasher = password_hasher

    def __call__(self, auth_login_input: AuthLoginInput) -> AuthLoginOutput:
        user = self.user_repository.get_by_email(auth_login_input.email)

        if user is None:
            # Run a dummy bcrypt check to normalise timing and prevent
            # user-enumeration attacks via response-time differences.
            self.password_hasher.dummy_verify(auth_login_input.password)
            raise InvalidCredentialsError()

        if not self.password_hasher.verify(auth_login_input.password, user.hashed_password):
            raise InvalidCredentialsError()

        token = self.jwt_service.create_token(user)

        return AuthLoginOutput(
            access_token=token,
            user_id=user.id,
            name=user.name,
            role=user.role.value,
        )
 