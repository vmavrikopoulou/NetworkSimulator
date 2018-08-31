from simulator.Exceptions import SimulatorException, SimulatorError
from simulator.topics.Topics import Topics


class InteractionCore:
    
    
    def __init__(self, name = "USER"):
        self.eventBus = None
        self.name = name
    
    def loadEventBus(self, eventBus):
        self.eventBus = eventBus
        
    def tick(self, time):
        raise SimulatorException(
            SimulatorError.IMPLEMENTATION_MISSING,
            "Method tick should be overloaded for a InteractionModule"
        )
    
    def sendMessage(self, message):
        self.eventBus.emit(Topics.interactionMessage, {"sender": self.name, "payload": message})