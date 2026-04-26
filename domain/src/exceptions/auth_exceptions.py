class InvalidCredentialsError(Exception):
    """Exception raised when login credentials are invalid."""
    def __init__(self, message: str = "Credenciales inválidas"):
        self.message = message
        super().__init__(self.message)
