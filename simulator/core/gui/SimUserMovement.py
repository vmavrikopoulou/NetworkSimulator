from simulator.util.JsonFileStore import JsonFileStore
from simulator.core.gui.GuiCore import SimulationEventBus
from simulator.topics.Topics import GuiTopics
import datetime

class SimUserMovement:
    
    def __init__(self, gui):
        self.gui = gui
        self.path = []
        
        SimulationEventBus.subscribe(GuiTopics.mousePress, self._handleMousePress)
        SimulationEventBus.subscribe(GuiTopics.keyPress, self._handleKeyPress)
        
    def _handleKeyPress(self, key):
        if self.gui.state["pathDrawing"] and len(self.path) > 0:
            self.path.pop()
        
    def _handleMousePress(self, pos):
        if self.gui.state["pathDrawing"]:
            posOnMap = (pos[0] - self.gui.mapPadding, pos[1] - self.gui.mapPadding)
            if posOnMap[0] < self.gui.mapWidth and posOnMap[1] < self.gui.mapHeight:
                self.path.append(self.gui.xyPixelsToMeters(posOnMap))

    def saveToFile(self):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S")
        store = JsonFileStore("userData_" + now + ".json", False)
        store.addEntry("path", self.path)
        store.addEntry("userWalkingSpeed", self.gui.config["userWalkingSpeed"])
        store.addEntry("intervalMs", 200)
        store.addEntry("address", "ff:00")
        store.addEntry("payload", "insertPayloadHere")
        self.gui.state["pathDrawing"] = False
    