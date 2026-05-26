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


class CustomerNotFoundError(Exception):
    """Exception raised when a customer with the given ID does not exist."""
    def __init__(self, message="Customer not found."):
        self.message = message
        super().__init__(self.message)


class CustomerUpdateError(Exception):
    """Exception raised when persisting a customer update fails."""
    def __init__(self, message="Failed to update customer."):
        self.message = message
        super().__init__(self.message)
