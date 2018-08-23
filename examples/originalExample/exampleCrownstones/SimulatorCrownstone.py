from simulator.simulatorBases.CrownstoneCore import CrownstoneCore
from simulator.simulatorBases.GuiCrownstoneCore import GuiCrownstoneCore


class SimulatorCrownstone(GuiCrownstoneCore):
    
    """
        Class variables are created here.
    """
    myValue = False
    
    def __init__(self, id, x, y):
        super().__init__(id=id,x=x,y=y)
       
    def resetState(self, resetTrainingData = True):
        """
            This is an important method to reset any state the Crownstone may have so the simulation can be restarted.
            If resetTrainingData is False, you should clear all state data except that referring to the training sets.
        """
        self.myValue = False
    
       
    # overloaded
    def receiveMessage(self, data, rssi):
        """
            This is where mesh messages are received
            :param data:  { "sender":string, "payload": dictionary }
        """
        print(self.id, "I HAVE A MESSAGE FROM", data["sender"], " SAYING ", data["payload"])

    # overloaded
    def newMeasurement(self, data, rssi):
        """
            This is where scanned ble devices are seen
            :param data:  { "address":string, "payload": dictionary }
        """
        print(self.time, self.id, "Scans indicate", data["address"], " with payload ", data["payload"], " and rssi:", rssi)
        
        if rssi > -45:
            self.sendMessage("I saw a beacon with more that -45 dB!" + str(rssi) + "   " + str(self.time))

        self.sendMessage("I measured something" + str(rssi) + "   " + str(self.time))
            