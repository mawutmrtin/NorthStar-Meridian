from dataclasses import dataclass
from typing import Optional


@dataclass
class StockItem:
    sku: str
    name: str
    quantity: int


@dataclass
class PrintJob:
    job_id: str
    attendee_id: str
    status: str = "queued"  # queued, pending, completed, failed
    attempt: int = 0
    error: Optional[str] = None
