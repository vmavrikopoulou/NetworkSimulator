# Every crownstone creates its ResultMap and no result is published in order to not influence the way that the testdata 
# is created for every crownstone. A confidence Map with the probabilities that correspond to each labelroom

from simulator.simulatorBases.CrownstoneCore import CrownstoneCore
from simulator.simulatorBases.GuiCrownstoneCore import GuiCrownstoneCore
import math
import operator
import string

class SimulatorCrownstone(GuiCrownstoneCore):
    """
        Class variables are created here.
    """

    # myValue = False

    def __init__(self, id, x, y):
        super().__init__(id=id, x=x, y=y)
        # self.debugPrint = False
        self.flag, self.label, self.counter, self.param, self.value, self.sign = 0, 0, 0, 0, 0, 0
        self.radiomap, self.predictions, self.testSet, self.probabilities, self.parameters = {}, {}, {}, {}, {}
        self.w, self.p, self.publish, self.resetTrainingData, self.timelimit = 0, 0, 0, 0, 0
        self.Map, self.confidence_Map = {}, {}
        self.nodes = 7

    # def print(self, data):
    #     if self.debugPrint:
    #         print(data)

    def resetState(self, resetTrainingData):
        # This is an important method to reset any state the Crownstone may have so the simulation can be restarted.
        # If resetTrainingData is False, you should clear all state data except that referring to the training sets.
        if resetTrainingData:
            self.flag, self.label, self.counter, self.sign = 0, 0, 0, 0
            self.radiomap = {}
            self.w, self.p, self.publish = 0, 0, 0
            self.param = 1
        else:
            self.counter, self.value, self.sign = 0, 0, 0
            self.predictions, self.testSet, self.probabilities = {}, {}, {}
            self.w, self.p = 0, 0
            self.param = 1
            self.publish, self.resetTrainingData = 1, 1
            self.timelimit = self.time
            self.flag = 2
        # self.print ("resetTrainingData" + str(self.time))

    def tick(self, time):
        # self.print("TICKY" + str(time) + "  " + str(self.time))
        # self.print("simTime" + str(self.time) + " limit: " + str(self.timelimit))
        # make predictions after 0.5 sec
        # the result map of each crownstone should be created after the crownstones have received the info from their neighbors
        if (self.time > self.timelimit + 0.5 and self.resetTrainingData == 1 and self.w == 1):
            self.timelimit = self.timelimit + 500
            if len(self.testSet) != 0:
                self.probabilities, self.predictions = self.Predictions()
                if self.predictions[0] == 1:
                    roomId = "Room 1"
                elif self.predictions[0] == 2:
                    roomId = "Room 2"
                elif self.predictions[0] == 3:
                    roomId = "Room 3"
                elif self.predictions[0] == 4:
                    roomId = "Room 4"
                elif self.predictions[0] == 5:
                    roomId = "Room 5"
                elif self.predictions[0] == 6:
                    roomId = "Room 6"
                elif self.predictions[0] == 7:
                    roomId = "Room 7"
                if 'x' in self.debugInformation:
                    x = int(self.debugInformation['x'])
                    y = int(self.debugInformation['y'])
                    # construct the result map of every crownstone
                    for key, values in self.Map.items():
                        if key == x:
                            for ck in values.keys():
                                if ck == y:
                                    self.Map[key][ck] = roomId
                    # construct the confidence map for every crownstone. store the probability with which the room was predicted.
                    for key, values in self.confidence_Map.items():
                        if key == x:
                            for ck in values.keys():
                                if ck == y:
                                    self.confidence_Map[key][ck] = self.probabilities[0]

    def receiveMessage(self, data, rssi):
        # print(self.time, "Crownstone", self.id, "received from crownstone", data["sender"], "with payload", data["payload"], " and rssi:", rssi)
        if data["payload"] == "StartTraining":
            self.label = self.label + 1
            self.radiomap[self.label] = {}
            self.flag = 1
        # When I receive "Start training" a flag informs the crownstones to start constructing their radio maps.
        if data["payload"] == "StopTraining":
            self.flag = 0
        if data["payload"] == "StartLocalizing":
            # the parameters (mean & standard deviation) to be calculated only once. flag: self.param
            self.param = 1
            self.flag = 2

        # both the radio map construction and the testSet construction are held in both receiveMessage and newMeasurement functions
        # as the radio map of each crownstone contains information (RSSI values) received from other crownstones. Either from all the crownstones
        # in the mesh network (all crownstones have the same data - highest ttl - fully connected graph) or from only their neighbours (ttl=1 - not fully connected graph).
        if (self.flag == 1):
            # Construction of radiomap.
            if 'rssi' in data['payload']:
                if data['payload']['originalSender'] not in self.radiomap[self.label]:
                    self.radiomap[self.label][data['payload']['originalSender']] = []
                self.radiomap[self.label][data['payload']['originalSender']].append(data['payload']['rssi'])

        if (self.flag == 2):
            # The parameters (mean & standard deviation) of each crownstone for each room are calculated only once after the end of the training phase.
            if self.param == 1:
                if len(self.parameters) == 0:
                    self.parameters = self.crownParameters(self.radiomap)
                    # Initialization of result map for every crownstone
                    self.Map, self.confidence_Map = {}, {}
                    for self.x in range(85, 735, 10):
                        self.Map[self.x] = {}
                        self.confidence_Map[self.x] = {}
                        for self.y in range(85, 855, 10):
                            self.Map[self.x][self.y] = None
                            self.confidence_Map[self.x][self.y] = None

            if self.w == 0:
                self.counter = self.counter + 1
                # self.testSet[self.counter]={}
                # for a complete testSet if a crownstone doesn't even scan the user, set RSSI to a really small value.
                # self.testSet[self.counter][self.id]=[-100]

            # Construction of testSet, the original sender of the packet is received and saved to the set.
            if 'rssi' in data['payload']:
                if self.counter not in self.testSet:
                    self.testSet[self.counter] = {}
                if data['payload']['originalSender'] not in self.testSet[self.counter]:
                    self.testSet[self.counter][data['payload']['originalSender']] = []
                self.testSet[self.counter][data['payload']['originalSender']].append(data['payload']['rssi'])
                # check if the testSet is complete. The lenght of each row should be equal to the number of nodes in the mesh network.
                if len(self.testSet[self.counter]) == self.nodes:
                    self.w = 0
                else:
                    self.w = 1

    def newMeasurement(self, data, rssi):
        # print(self.time, self.id, "scans", data["address"], " with payload ", data["payload"], " and rssi:", rssi)
        if (self.flag == 1):
            self.sendMessage({"rssi": rssi, "originalSender": self.id}, 1)
            # Construction of radio map
            if self.id not in self.radiomap[self.label]:
                self.radiomap[self.label][self.id] = []
            self.radiomap[self.label][self.id].append(rssi)

        if (self.flag == 2):
            # Construction of testSet. If the crownstone is able to scan the user the flag w is set to 1, otherwise it remains 0.
            # flag p is used to avoid retransmissions
            if self.p == 0:
                self.counter = self.counter + 1
                self.w = 1
                if self.counter not in self.testSet:
                    self.testSet[self.counter] = {}
                if self.id not in self.testSet[self.counter]:
                    self.testSet[self.counter][self.id] = []
                self.testSet[self.counter][self.id].append(rssi)
                self.value = self.testSet[self.counter][self.id][0]
                self.sendMessage({"rssi": rssi, "originalSender": self.id}, 1)
                self.p = 1
            if rssi != self.value:
                self.counter = self.counter + 1
                self.w = 1
                if self.counter not in self.testSet:
                    self.testSet[self.counter] = {}
                if self.id not in self.testSet[self.counter]:
                    self.testSet[self.counter][self.id] = []
                self.testSet[self.counter][self.id].append(rssi)
                self.sendMessage({"rssi": rssi, "originalSender": self.id}, 1)

    def crownParameters(self, radiomap):
        parameters = {}
        for self.label, crowns in self.radiomap.items():
            if self.label not in parameters:
                parameters[self.label] = {}
            sorted_crowns = sorted(crowns.items(), key=operator.itemgetter(0))
            for crown, RSSI in sorted_crowns:
                if len(RSSI) != 1:
                    if crown not in parameters[self.label]:
                        parameters[self.label][crown] = []
                        parameters[self.label][crown] = self.Statistics(RSSI)
        return parameters

    def Statistics(self, RSSI):
        parameters = [self.MeanValue(RSSI), self.StandardDeviation(RSSI)]
        return parameters

    def MeanValue(self, rss):
        mean = sum(rss) / float(len(rss))
        return mean

    def StandardDeviation(self, rss):
        average = self.MeanValue(rss)
        variance = sum([pow(RSSI - average, 2) for RSSI in rss]) / float(len(rss) - 1)
        standarddev = math.sqrt(variance)
        return standarddev

    def Predictions(self):
        predictions = []
        probabilities = []
        for counter in self.testSet:
            best_probability, room_label = self.PredictRoom(self.testSet[counter])
            probabilities.append(best_probability)
            predictions.append(room_label)
        return probabilities, predictions

    # def Predictions_norm(self, parameters, testSet):
    #     predictions = []
    #     for counter in self.testSet:
    #         room_label = self.PredictRoom_norm(self.parameters, self.testSet[counter])
    #         predictions.append(room_label)
    #     return predictions

    def PredictRoom(self, testSet):
        probabilities = self.RoomProbabilities(testSet)
        room_predicted, best_probability = None, -1
        for room_label, probability in probabilities.items():
            if room_predicted is None or probability > best_probability:
                best_probability = probability
                room_predicted = room_label
        return best_probability, room_predicted

    # def PredictRoom_norm(self, parameters, testSet):
    #     probabilities = self.RoomProbabilities_norm(self.parameters, testSet)
    #     room_predicted, best_probability = None, -1
    #     for room_label, probability in probabilities.items():
    #         if room_predicted is None or probability > best_probability:
    #             best_probability = probability
    #             room_predicted = room_label
    #     return room_predicted

    def RoomProbabilities(self, testSet):
        probabilities = {}
        n = 0
        for self.label, room_parameters in self.parameters.items():
            probabilities[self.label] = 1
            for crown in room_parameters.items():
                for node, rssi in testSet.items():
                    if crown[0] == node:
                        mean = crown[1][0]
                        standardev = crown[1][1]
                        exponent_numerator = math.pow(rssi[0] - mean, 2)
                        exponent_denominator = 2 * math.pow(standardev, 2)
                        exponent_result = math.exp((-exponent_numerator) / exponent_denominator)
                        prob_density = (1 / (math.sqrt(2 * math.pi) * standardev)) * exponent_result
                        probabilities[self.label] *= prob_density
                        n = n + 1
        return probabilities

    # def RoomProbabilities_norm(self, parameters, testSet):
    #     probabilities1={}
    #     norm_factor={}
    #     norm_probabilities={}
    #     for self.label, room_parameters in self.parameters.items():
    #         probabilities1[self.label]= {}
    #         for crown in room_parameters.items():
    #             if crown[0] not in probabilities1[self.label]:
    #                 probabilities1[self.label][crown[0]]=[]
    #             probabilities1[self.label][crown[0]].append(1)
    #             for node, rssi in testSet.items():
    #                 if crown[0] == node:
    #                     mean=crown[1][0]
    #                     standardev=crown[1][1]
    #                     exponent_numerator = math.pow(rssi[0]-mean,2)
    #                     exponent_denominator = 2*math.pow(standardev,2)
    #                     exponent_result = math.exp((-exponent_numerator)/exponent_denominator)
    #                     prob_density = (1 / (math.sqrt(2*math.pi) * standardev)) * exponent_result
    #                     #non-normalized probabilities
    #                     #product of our prior distribution
    #                     probabilities1[self.label][node][0] *= prob_density
    #     #normalization_factor one for each crownstone, sum of non-normalized probabilities for all rooms
    #     n=1
    #     for self.label, prob in probabilities1.items():
    #         for node in prob.items():
    #             if n <= len(prob):
    #                 norm_factor[node[0]] = node[1][0]
    #                 n=n+1
    #             else:
    #                 norm_factor[node[0]] += node[1][0]
    #         #print ("normalization_factor", norm_factor)
    #     for self.label, prob in probabilities1.items():
    #         norm_probabilities[self.label]=1
    #         for node in prob.items():
    #             norm_probabilities[self.label] *= (1/ norm_factor[node[0]])* node[1][0]
    #     #print ("norm_probabilities",norm_probabilities)
    #     return norm_probabilities

    def Accuracy(self, testSet, predictions):
        correct = 0
        room = 5
        for x in range(len(predictions)):
            if room == (predictions[x]):
                correct += 1
        return (correct / float(len(predictions))) * 100.0
