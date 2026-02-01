from enum import Enum

class RepasseStatus(str, Enum):
    PENDING = "pending"
    CONSOLIDATED = "consolidated"
