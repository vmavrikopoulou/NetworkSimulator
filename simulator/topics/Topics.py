from enum import Enum

class Topics(Enum):
    meshMessage = "meshMessage"

class GuiTopics(Enum):
    mousePress = "mousePress"
    keyPress   = "keyPress"