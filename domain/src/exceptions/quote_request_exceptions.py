class CaptchaValidationError(Exception):
    """Exception raised when CAPTCHA validation fails."""
    def __init__(self, message="CAPTCHA validation failed."):
        self.message = message
        super().__init__(self.message)

class InvalidEmailError(Exception):
    """Exception raised when an email address is invalid."""
    def __init__(self, message="Invalid email address provided."):
        self.message = message
        super().__init__(self.message)

class EmailSendingError(Exception):
    """Exception raised when email sending fails."""
    def __init__(self, message="Failed to send email."):
        self.message = message
        super().__init__(self.message)
        