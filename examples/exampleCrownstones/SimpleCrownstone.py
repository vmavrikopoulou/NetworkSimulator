from simulator.simulatorBases.CrownstoneCore import CrownstoneCore

class SimpleCrownstone(CrownstoneCore):
    
    def __init__(self, id):
        super().__init__(id=id)
       
    
       
    # overloaded
    def receiveMessage(self, data):
        print(self.id, "I HAVE A MESSAGE FROM", data["sender"], " SAYING ", data["payload"])

    # overloaded
    def newMeasurement(self, data):
        print(self.time, self.id, "Scans indicate", data["address"], " with payload ", data["payload"], " and rssi:", data["rssi"])
        
        if data['rssi'] > -45:
            self.sendMessage("I saw a beacon with more that -45 dB!")