from simulator.core.gui.GuiCore import SimulationEventBus
from simulator.simulatorBases.BroadcasterCore import BroadcasterCore
from simulator.topics.Topics import GuiTopics
import math, time


class SimResultBroadcaster(BroadcasterCore):
    
    def __init__(self, address, pos, gui):
        super().__init__(address=address)
        self.gui = gui
        self.pos = pos
    
    def getRssiToCrownstone(self, targetCrownstoneId):
        targetCrownstone = self.gui.simulatorCrownstonesMap[targetCrownstoneId]
        rssi = self.gui.simMath.getRssiToPosition(targetCrownstone.pos, self.pos)
        return rssi
    