from simulator.simulatorBases.CrownstoneCore import CrownstoneCore
from simulator.simulatorBases.GuiCrownstoneCore import GuiCrownstoneCore


class SimulatorCrownstone(GuiCrownstoneCore):
    
    def __init__(self, id, x, y):
        super().__init__(id=id,x=x,y=y)
       
    # overloaded
    def receiveMessage(self, data):
        print(self.id, "I HAVE A MESSAGE FROM", data["sender"], " SAYING ", data["payload"])

    # overloaded
    def newMeasurement(self, data):
        print(self.time, self.id, "Scans indicate", data["address"], " with payload ", data["payload"], " and rssi:", data["rssi"])
        
        if data['rssi'] > -45:
            self.sendMessage("I saw a beacon with more that -45 dB!")