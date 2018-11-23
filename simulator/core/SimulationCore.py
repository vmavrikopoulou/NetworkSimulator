from simulator.Exceptions import SimulatorException, SimulatorError
from simulator.core.gui.SimMath import SimMath
from simulator.topics.Topics import Topics
from simulator.util.Enums import MessageState
from simulator.util.EventBus import EventBus
import uuid, random

class SimulationCore:
    
    def __init__(self):
        self.interactionModule = None
        self.crownstones = []
        self.crownstoneMap = {}
        self.deliveredCrownstoneMap = {}
        self.deliveredMessageMap = {}
        self.crownstoneRssiMap = {}
        self.crownstoneTopologyMap = {}
        self.messageCounter = 0
        self.transmissionDelay = 0
        
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
        self.deliveredCrownstoneMap = {}
        for crownstone in self.crownstones:
            self.deliveredCrownstoneMap[crownstone.id] = set()
        
        # add new eventBus
        newEventBus = EventBus()
        self.changeEventBus(newEventBus)

    def _abortSimulation(self, data):
        self.abort = True

    def loadConfig(self, config):
        self.config = config
        self.transmissionDelay = self.config["transmissionDelayInSeconds"]

    def changeEventBus(self, eventBus):
        self.eventBus = eventBus
        
        for crownstone in self.crownstones:
            crownstone.loadEventBus(self.eventBus)
            
        for broadcaster in self.broadcasters:
            broadcaster.loadEventBus(self.eventBus)
        
        self.eventBus.subscribe(Topics.interactionMessage, self._collectInteractionHandlerMessage)
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
            self.deliveredCrownstoneMap[crownstone.id] = set()
        
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
            
        self.constructTopology()
        
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
        relayMessages = []
        deleteList = []
        messageIds = list(self.messages.keys())
        for mId in messageIds:
            # ignore any messages that have been sent this round
            if self.messages[mId]["sentTime"] + self.transmissionDelay < self.t:
                status = self.handleMessage(self.messages[mId])
                if status == MessageState.DELIVERED:
                    relayMessages.append(mId)
                    
                if status != MessageState.DELAYED:
                    self.messages[mId]["processed"] = True
                    deleteList.append(mId)
                    
        for mId in relayMessages:
            self._relayMessage(self.messages[mId])
            
        # clean up messages that have been successfully handled.
        for mId in deleteList:
            self.messages.pop(mId)
                
    
    def handleMessage(self, message):
        self.handleMessageCounter += 1
        
        receiverId = message["receiverId"]
        senderId = message["senderId"]
        
        rssi = None
        receiver = None
        
        if senderId in self.crownstoneMap:
            receiver = self.crownstones[self.crownstoneMap[receiverId]]
            
            rssi = self.crownstoneRssiMap[senderId][receiverId]
        else:
            # these are messages from the interaction module
            if receiverId in self.crownstoneMap:
                receiver = self.crownstones[self.crownstoneMap[receiverId]]
                receiver.receiveMessage({"sender": message["senderId"], "payload": message["payload"], "ttl": 0}, rssi)
                return MessageState.DELIVERED_AT_ENDPOINT
            
        if rssi is None:
            return MessageState.UNREACHABLE
        else:
            # deliver the message
            # the ttl has been reduced by 1 since it has been sent once.
            self.receivedCounter += 1
            receiver.receiveMessage({"sender": message["senderId"], "payload": message["payload"], "ttl": message["ttl"] - 1}, rssi)
            
            if random.random() < float(self.config["messageLossProbability"]):
                message["repeat"] -= 1
                if message["repeat"] < 0:
                    return MessageState.FAILED
                
                return MessageState.DELAYED
            
            
            if message["ttl"] > 1:
                return MessageState.DELIVERED
            else:
                return MessageState.DELIVERED_AT_ENDPOINT
        
    def _relayMessage(self, message):
        # relay based on the TTL counter
        if self.deliveredMessageMap[message["messageId"]] == len(self.crownstones) - 1:
            return
    
        
        self._collectMessage({
            "messageId": message["messageId"],
            "payload": message["payload"],
            "sender": message["receiverId"], # the receiver is now the sender
            "ttl": message["ttl"] - 1,
        })
        
    receivedCounter = 0
    handleMessageCounter = 0
    collectMessageCounter = 0
    skipCounter = 0
    
    def _collectInteractionHandlerMessage(self, messageData):
        self.messageCounter += 1
        sourceId = self.messageCounter
        
        for crownstone in self.crownstones:
            self.messages[str(self.messageCounter) + "_" + str(crownstone.id)] = {
                "messageId": sourceId,
                "payload": messageData["payload"],
                "senderId": messageData["sender"],
                "receiverId": crownstone.id,
                "sentTime": self.t,
                "ttl": 1,
                "processed": False
            }
    
    
    def _collectMessage(self, messageData):
        self.collectMessageCounter += 1
        ttl = messageData["ttl"]
        
        self.messageCounter += 1
        sourceId = self.messageCounter
        if "messageId" in messageData:
            sourceId = messageData["messageId"]
        else:
            self.deliveredMessageMap[sourceId] = 0

        # we add the original sender to the delivered map so it won't get his own message when the sender changes
        self.deliveredCrownstoneMap[messageData["sender"]].add(sourceId)
        
        for crownstoneId in self.crownstoneTopologyMap[messageData["sender"]]:
            if sourceId in self.deliveredCrownstoneMap[crownstoneId]:
                self.skipCounter += 1
                continue
            
            self.deliveredCrownstoneMap[crownstoneId].add(sourceId)
            self.deliveredMessageMap[sourceId] += 1
            self.messages[str(self.messageCounter) + "_" + str(crownstoneId)] = {
                "messageId":  sourceId,
                "payload":    messageData["payload"],
                "senderId":   messageData["sender"],
                "receiverId": crownstoneId,
                "sentTime":   self.t,
                "ttl":        ttl,
                "processed":  False
            }
        
        
        
    
    def constructTopology(self):
        # get the rssi between Crownstones
        self.crownstoneTopologyMap = {}
        self.crownstoneRssiMap = {}
        self.deliveredCrownstoneMap = {}

        for crownstone in self.crownstones:
            self.crownstoneTopologyMap[crownstone.id] = []
            self.deliveredCrownstoneMap[crownstone.id] = set()
            for targetCrownstone in self.crownstones:
                if crownstone.id != targetCrownstone.id:
                    if crownstone.id not in self.crownstoneRssiMap:
                        self.crownstoneRssiMap[crownstone.id] = {}
                    
                    if targetCrownstone.id not in self.crownstoneRssiMap[crownstone.id]:
                        self.crownstoneRssiMap[crownstone.id][targetCrownstone.id] = self._getRssiBetweenCrownstones(crownstone, targetCrownstone)
                    
                    rssi = self.crownstoneRssiMap[crownstone.id][targetCrownstone.id]
                    
                    if rssi is not None:
                        self.crownstoneTopologyMap[crownstone.id].append(targetCrownstone.id)
                

    def _getRssiBetweenCrownstones(self, crownstone1, crownstone2):
        distance = SimMath.getDistanceBetweenCrownstones(crownstone1, crownstone2)
        rssiCalibration = self.config["rssiCalibrationCrownstone"]
        NValue = self.config["nValueCrownstone"]
    
    
        # there is no noise here to ensure that the topology is good.
        return SimMath.getRSSI(rssiCalibration, NValue, distance, self.config["rssiMinimumCrownstone"], 0)
        
    
    
