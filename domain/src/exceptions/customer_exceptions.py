class InvalidCustomerDataError(Exception):
    """Exception raised when customer input data is invalid."""
    def __init__(self, message="Invalid customer data."):
        self.message = message
        super().__init__(self.message)


class CustomerCreationError(Exception):
    """Exception raised when persisting a customer fails."""
    def __init__(self, message="Failed to create customer."):
        self.message = message
        super().__init__(self.message)
