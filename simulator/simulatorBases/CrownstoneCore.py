from simulator.topics.Topics import Topics


class CrownstoneCore:
    id = None
    eventBus = None
    time = 0
    
    def __init__(self, id):
        self.id = id
        
    def setTime(self, time):
        self.time = time

    def loadEventBus(self, eventBus):
        self.eventBus = eventBus
    
    def sendMessage(self, data):
        self.eventBus.emit(Topics.meshMessage, {"sender": self.id, "payload": data})
    
    def receiveMessage(self, data):
        pass
    
    def newMeasurement(self, data):
        pass
    
    def tick(self, time):
        pass
    
    def getResult(self, roomId):
        self.eventBus.emit(Topics.gotResult, {"sender": self.id, "roomId": roomId})
        
    def resetState(self, resetTrainingData = True):
        pass