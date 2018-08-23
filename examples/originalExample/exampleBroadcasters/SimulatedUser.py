from simulator.simulatorBases.BroadcasterCore import BroadcasterCore
import numpy

class SimulatedUser(BroadcasterCore):
    path = None
    
    def __init__(self, address):
        super().__init__(address="address")
        
    def loadPath(self, path):
        self.path = path
    