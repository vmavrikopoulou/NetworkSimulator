from simulator.simulatorBases.BroadcasterCore import BroadcasterCore
import numpy

class IBeacon(BroadcasterCore):
    
    targetParameters = None
    
    def __init__(self, address):
        super().__init__(address="address")
        
    def setTargetParameters(self, crownstoneDictionary):
        self.targetParameters = crownstoneDictionary
    
    # override
    def getRssiToCrownstone(self, targetCrownstoneId):
        """
        This method will be repeatedly called by the simulatorCore
        :param targetCrownstoneId: This is an ID of the Crownstones loaded into the Core
        :return: Number or None
        """
    
        if self.targetParameters is None:
            return None
    
        if targetCrownstoneId not in self.targetParameters:
            return None
    
        params = self.targetParameters[targetCrownstoneId]
        rssi = numpy.random.normal(params["mean"], params["std"])
    
        return rssi
