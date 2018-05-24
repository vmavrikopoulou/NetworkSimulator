from enum import Enum

class MessageState(Enum):
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"
    DELAYED = "DELAYED"