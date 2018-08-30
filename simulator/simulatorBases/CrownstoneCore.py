from simulator.topics.Topics import Topics


class CrownstoneCore:
    def __init__(self, id):
        self.id = id
        self.eventBus = None
        self.time = 0
        self.debugPrint = False

    def print(self, *data):
        if self.debugPrint:
            print(data)
        
    def setTime(self, time):
        self.time = time

    def loadEventBus(self, eventBus):
        self.eventBus = eventBus
    
    def sendMessage(self, data):
        self.eventBus.emit(Topics.meshMessage, {"sender": self.id, "payload": data})
    
    def receiveMessage(self, data, rssi):
        pass
    
    def newMeasurement(self, data, rssi):
        pass
    
    def tick(self, time):
        pass
    
    def publishResult(self, roomId):
        self.eventBus.emit(Topics.gotResult, {"sender": self.id, "roomId": roomId})
        
    def resetState(self, resetTrainingData = True):
        pass