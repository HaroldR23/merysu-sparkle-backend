from dataclasses import dataclass

@dataclass
class QuoteRequestInput:
    customer_name: str
    customer_email: str
    service_details: str
    customer_message: str
