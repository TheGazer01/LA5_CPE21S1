"""A record of one processed payment."""
import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Transaction:
    payer: str
    method: str
    amount: float
    message: str
    success: bool
    txn_id: str = field(default_factory=lambda: uuid.uuid4().hex[:10].upper())
    timestamp: datetime = field(default_factory=datetime.now)

    @property
    def status(self):
        return "SUCCESS" if self.success else "FAILED"

    @property
    def time_str(self):
        return self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
