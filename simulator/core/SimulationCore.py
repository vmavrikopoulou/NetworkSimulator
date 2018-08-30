from simulator.Exceptions import SimulatorException, SimulatorError
from simulator.core.gui.SimMath import SimMath
from simulator.topics.Topics import Topics
from simulator.util.Enums import MessageState
from simulator.util.EventBus import EventBus
import uuid

class SimulationCore:
    
    def __init__(self):
        self.interactionModule = None
        self.crownstones = []
        self.crownstoneMap = {}
        self.broadcasters = []
    
        self.eventBus = None
    
        self.guiMode = None
        self.config = None
    
        self.messages = {}
    
        self.t = 0  # time in seconds
        self.abort = False
        
        self.restart()

    def restart(self):
        if self.eventBus is not None:
            self.eventBus.destroy()
    
        # clear all messages
        self.messages = {}
        
        # add new eventBus
        newEventBus = EventBus()
        self.changeEventBus(newEventBus)

    def _abortSimulation(self, data):
        self.abort = True

    def loadConfig(self, config):
        self.config = config

    def changeEventBus(self, eventBus):
        self.eventBus = eventBus
        
        for crownstone in self.crownstones:
            crownstone.loadEventBus(self.eventBus)
            
        for broadcaster in self.broadcasters:
            broadcaster.loadEventBus(self.eventBus)

        self.eventBus.subscribe(Topics.meshMessage, self._collectMessage)
        self.eventBus.subscribe(Topics.gotResult, self._abortSimulation)
    
    def loadInteractionModule(self, interactionModule):
        """
            This will load an interaction module into the core
            :param interactionModule: instance inheriting the InteractionCore class
            :return:
        """
        self.interactionModule = interactionModule
        self.interactionModule.loadEventBus(self.eventBus)

    def loadCrownstones(self, crownstones):
        """
            This will load the Crownstone simulators into the core
            :param crownstones: List of class instances that inherit the CrownstoneCore class
            :return:
        """
        self.crownstones = crownstones
        index = 0
        for crownstone in self.crownstones:
            self.crownstoneMap[crownstone.id] = index
            index += 1
            crownstone.loadEventBus(self.eventBus)
        
    def loadBroadcasters(self, broadcasters):
        """
            This will load the Broadcaster simulators into the core.
            Broadcasters can be phones, ibeacons, etc. They inherit the BroadcasterCore class
            :param broadcasters: List of class instances that inherit the BroadcasterCore class
            :return:
        """
        self.broadcasters = broadcasters
        for broadcaster in self.broadcasters:
            broadcaster.loadEventBus(self.eventBus)
            
            
    def resetSimulatorForResults(self):
        self.broadcasters = []
        self.interactionModule = None
        self.restart()
        self.loadCrownstones(self.crownstones)
        
        for crownstone in self.crownstones:
            crownstone.resetState(resetTrainingData=False)

    def start(self, duration, timeStep = 0.01):
        """
        Start simulation
            :param duration: simulation time in seconds
            :param timeStep: time step size in milliseconds
            :return:
        """
        for crownstone in self.crownstones:
            crownstone.resetState(True)
            
        if timeStep <= 0:
            raise SimulatorException(SimulatorError.USER_INPUT_ERROR, "Invalid Step size. Must be larger than 0.")
        
        self.t = 0
        self.abort = False
        while self.t < duration and self.abort == False:
            self.tick()
            self.t = self.t + timeStep
    
    def continueSimulation(self, duration, timeStep = 0.01):
        """
            Continue simulation
            :param duration: simulation time in seconds
            :param timeStep: time step size in milliseconds
            :return:
        """
        if timeStep <= 0:
            raise SimulatorException(SimulatorError.USER_INPUT_ERROR, "Invalid Step size. Must be larger than 0.")
        
        startT = self.t

        self.abort = False
    
        while self.t < (startT + duration) and self.abort == False:
            self.tick()
            self.t = self.t + timeStep
    
    
    def tick(self):
        # update the time of this step for all members of the simulation
        for crownstone in self.crownstones:
            crownstone.setTime(self.t)
            crownstone.tick(self.t)
          
        for broadcaster in self.broadcasters:
            broadcaster.setTime(self.t)
            broadcaster.tick(self.t)
            
        # first step is for the simulation interaction module to do things.
        if self.interactionModule is not None:
            self.interactionModule.tick(self.t)
        
        # second step is to ask all broadcasters to send a message
        for broadcaster in self.broadcasters:
            if broadcaster.willBroadcastMessage:
                for crownstone in self.crownstones:
                    messageResult = broadcaster.generateMessage(crownstone.id)
                    if messageResult is not None:
                        crownstone.newMeasurement(messageResult[0], messageResult[1])
                    
        # last step we deliver all messages that were sent in the last round.
        messageIds = list(self.messages.keys())
        for mId in messageIds:
            # ignore any messages that have been sent this round
            if self.messages[mId]["sentTime"] < self.t:
                for crownstone in self.crownstones:
                    status = self.handleMessage(self.messages[mId], crownstone)
                    if status == MessageState.DELIVERED or status == MessageState.SKIPPED:
                        self.messages[mId]["handled"][crownstone.id] = True
                    elif status == MessageState.FAILED:
                        self.messages[mId]["handled"][crownstone.id] = False
                        

        # clean up messages that have been successfully handled.
        for mId in messageIds:
            finished = True
            for crownstone in self.crownstones:
                if crownstone.id not in self.messages[mId]["handled"]:
                    finished = False
                    break
            if finished:
                # print("Clean up message", mId)
                self.messages.pop(mId)
                
    
    
    
    def handleMessage(self, message, receiver):
        """
        This can be overridden to implement delays, topology, failures, etc.
        :param message:
        :param receiver:
        :return:
        """
        
        receiverId = receiver.id
        if message["sender"] == receiverId:
            return MessageState.SKIPPED
        
        senderId = message["sender"]
        rssi = None
        if senderId in self.crownstoneMap:
            sender = self.crownstones[self.crownstoneMap[senderId]]
            
            rssi = self._getRssiBetweenCrownstones(sender,receiver)
        
        
        ##
        # HERE we can put code that checks topology, then sets the expected time of arrival and compares this with the current time
        # If it is delayed, we will return:
        # return MessageState.DELAYED
        ##
        
        
        receiver.receiveMessage(message, rssi)
        return MessageState.DELIVERED
    
    
    def _collectMessage(self, messageData):
        messageId = str(uuid.uuid4())
        self.messages[messageId] = {
            "payload": messageData["payload"],
            "sender": messageData["sender"],
            "sentTime": self.t,
            "handled": {}
        }
        
    def _getRssiBetweenCrownstones(self, crownstone1, crownstone2):
        distance = SimMath.getDistanceBetweenCrownstones(crownstone1, crownstone2)
        rssiCalibration = self.config["rssiCalibrationCrownstone"]
        NValue = self.config["nValueCrownstone"]
    
        return SimMath.getRSSI(rssiCalibration, NValue, distance, self.config["rssiMinimumCrownstone"])
        
    
    
