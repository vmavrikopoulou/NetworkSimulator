from enum import Enum

class Topics(Enum):
    meshMessage = "meshMessage"
    gotResult = "gotResult"

class GuiTopics(Enum):
    mousePress = "mousePress"
    keyPress   = "keyPress"