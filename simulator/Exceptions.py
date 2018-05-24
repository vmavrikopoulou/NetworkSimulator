from enum import Enum


class SimulatorError(Enum):
    CAN_NOT_FIND_SERVICE             = "CAN_NOT_FIND_SERVICE"
    ERROR                            = "ERROR"
    USER_INPUT_ERROR                 = "USER_INPUT_ERROR"
    IMPLEMENTATION_MISSING           = "IMPLEMENTATION_MISSING"
    IMPLEMENTATION_ERROR             = "IMPLEMENTATION_ERROR"

class SimulatorException(Exception):
    code    = None
    type    = None
    message = None
    
    def __init__(self, type, message, code=0):
        self.type = type
        self.message = message
        self.code = code
