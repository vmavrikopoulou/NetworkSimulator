from simulator.Exceptions import SimulatorException, SimulatorError
import random

class BroadcasterCore:
    
    address = None
    intervalMs = None
    payload = None
    
    eventBus = None
    willBroadcastMessage = False
    
    timeLastBroadcast = 0
    
    def __init__(self, address):
        self.timeLastBroadcast = random.random()
        self.address = address

    def loadEventBus(self, eventBus):
        self.eventBus = eventBus
        
    def setBroadcastParameters(self, intervalMs, payload):
        self.intervalMs = intervalMs
        self.payload = payload
        
    def changePayload(self, payload):
        self.payload = payload
        
    def generateMessage(self, targetCrownstoneId):
        rssi = self.getRssiToCrownstone(targetCrownstoneId)
        
        if rssi is None:
            return None
        
        return { "address": self.address, "payload" : self.payload, "rssi": rssi }
    
    def getRssiToCrownstone(self, targetCrownstoneId):
        raise SimulatorException(
            SimulatorError.IMPLEMENTATION_MISSING,
            "Method getRssiToCrownstone should be overloaded for a Broadcaster"
        )
        
    def setTime(self, time):
        self.willBroadcastMessage = False
        if time - self.timeLastBroadcast > self.intervalMs*0.001:
            self.timeLastBroadcast = time
            self.willBroadcastMessage = True
            
    def tick(self, time):
        pass
    
    