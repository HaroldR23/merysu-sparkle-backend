class InvalidServiceDataError(Exception):
    """Exception raised when service input data is invalid."""

    def __init__(self, message="Invalid service data."):
        self.message = message
        super().__init__(self.message)


class ServiceCreationError(Exception):
    """Exception raised when persisting a service fails."""

    def __init__(self, message="Failed to create service."):
        self.message = message
        super().__init__(self.message)


class ServiceNotFoundError(Exception):
    """Exception raised when a service cannot be found."""

    def __init__(self, message="Service not found."):
        self.message = message
        super().__init__(self.message)


class ServiceUpdateError(Exception):
    """Exception raised when updating a service fails."""

    def __init__(self, message="Failed to update service."):
        self.message = message
        super().__init__(self.message)
