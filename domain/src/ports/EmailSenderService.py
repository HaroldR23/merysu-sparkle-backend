from abc import ABC, abstractmethod

class EmailSenderService(ABC):
    @abstractmethod
    async def send_email(self, recipient: str, subject: str, body: str) -> None:
        """Send an email to the specified recipient."""
        pass
