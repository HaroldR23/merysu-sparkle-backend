from typing import cast
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from adapters.src.models.UserModel import UserModel
from domain.src.entities.user import User, UserRole
from domain.src.ports.repositories.UserRepository import UserRepository


class UserRepositoryAdapter(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def _to_domain(self, db_user: UserModel) -> User:
        return User(
            id=cast(UUID, db_user.id),
            email=db_user.email,
            name=db_user.name,
            role=UserRole(db_user.role),
            hashed_password=db_user.hashed_password,
        )

    def get_by_email(self, email: str) -> User | None:
        stmt = select(UserModel).where(UserModel.email == email)
        db_user = self.session.execute(stmt).scalar_one_or_none()
        if db_user is None:
            return None
        return self._to_domain(db_user)

    def create(self, user: User) -> User:
        db_user = UserModel(
            email=user.email,
            name=user.name,
            role=user.role.value,
            hashed_password=user.hashed_password,
        )
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return self._to_domain(db_user)
