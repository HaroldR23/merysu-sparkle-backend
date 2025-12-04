from pydantic import BaseModel, EmailStr

class QuoteRequestDTO(BaseModel):
    name: str
    service: str
    email: EmailStr
    message: str
    captcha_token: str
