class InvalidEmployeeDataError(Exception):
    """Exception raised when employee input data is invalid."""
    def __init__(self, message="Invalid employee data."):
        self.message = message
        super().__init__(self.message)


class EmployeeCreationError(Exception):
    """Exception raised when persisting an employee fails."""
    def __init__(self, message="Failed to create employee."):
        self.message = message
        super().__init__(self.message)
