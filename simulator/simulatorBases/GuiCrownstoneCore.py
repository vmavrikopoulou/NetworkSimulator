from simulator.simulatorBases.CrownstoneCore import CrownstoneCore


class GuiCrownstoneCore(CrownstoneCore):
    
    def __init__(self, id, x, y):
        super().__init__(id)
        self.pos = (x,y)
        
        