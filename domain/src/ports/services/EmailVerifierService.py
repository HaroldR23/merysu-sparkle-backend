from abc import ABC, abstractmethod

class EmailVerifierService(ABC):
    
    @abstractmethod
    async def verify_email(self, email: str) -> bool:
        """Verify if the provided domain email address is valid."""
        pass
