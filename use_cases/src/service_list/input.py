from dataclasses import dataclass
from datetime import date


@dataclass
class ServiceListInput:
    search: str | None = None
    date_from: date | None = None
    date_to: date | None = None
    page: int = 1
    page_size: int = 20
