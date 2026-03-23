from abc import ABC, abstractmethod


class CaptchaService(ABC):
    @abstractmethod
    async def verify(self, token: str) -> dict:
        """Verify the provided CAPTCHA token."""
        pass
