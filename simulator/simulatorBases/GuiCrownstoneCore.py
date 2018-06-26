from simulator.simulatorBases.CrownstoneCore import CrownstoneCore
from simulator.topics.Topics import Topics


class GuiCrownstoneCore(CrownstoneCore):
    pos = None
    
    def __init__(self, id, x, y, z):
        super().__init__(id)
        self.pos = (x,y,z)
        