from enum import Enum

class MessageState(Enum):
    DELIVERED_AT_ENDPOINT = "DELIVERED_AT_ENDPOINT"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"
    DELAYED = "DELAYED"
    ALREADY_DELIVERED = "ALREADY_DELIVERED"
    SKIPPED = "SKIPPED"
    UNREACHABLE = "UNREACHABLE"