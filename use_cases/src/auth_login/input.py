from dataclasses import dataclass


@dataclass
class AuthLoginInput:
    email: str
    password: str
