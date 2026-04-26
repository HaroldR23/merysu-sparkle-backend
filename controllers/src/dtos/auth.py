from uuid import UUID

from pydantic import BaseModel, EmailStr


class LoginRequestDTO(BaseModel):
    email: EmailStr
    password: str


class UserInfoDTO(BaseModel):
    id: str
    name: str
    role: str


class LoginResponseDTO(BaseModel):
    access_token: str
    user: UserInfoDTO
