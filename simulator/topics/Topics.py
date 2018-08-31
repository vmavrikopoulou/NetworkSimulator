from enum import Enum

class Topics(Enum):
    interactionMessage = "interactionMessage"
    meshMessage = "meshMessage"
    gotResult = "gotResult"

class GuiTopics(Enum):
    mousePress = "mousePress"
    keyPress   = "keyPress"