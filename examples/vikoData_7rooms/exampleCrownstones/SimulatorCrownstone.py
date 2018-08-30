from simulator.simulatorBases.CrownstoneCore import CrownstoneCore
from simulator.simulatorBases.GuiCrownstoneCore import GuiCrownstoneCore
import math
import operator
import string

class SimulatorCrownstone(GuiCrownstoneCore):
    
    """
        Class variables are created here.
    """
    #myValue = False
    
    
    def __init__(self, id, x, y):
        super().__init__(id=id,x=x,y=y)
        #self.debugPrint = False
        self.flag = 0 
        self.radiomap = {}
        self.label= 0
        self.predictions={}
        #self.predictions_norm={}
        self.testSet = {}
        self.counter = 0
        self.sign= 0
        self.test_dataset = 0
        self.n=0
        self.k=0
        self.publish=0

    def print(data):
        if self.debugPrint:
            print(data)

    def resetState(self, resetTrainingData):
        #This is an important method to reset any state the Crownstone may have so the simulation can be restarted.
        #If resetTrainingData is False, you should clear all state data except that referring to the training sets.
        if resetTrainingData:
            self.flag = 0 
            self.radiomap ={}
            self.label= 0
            self.predictions={}
            #self.predictions_norm={}
            self.testSet = {}
            self.counter = 0
            self.sign= 0
            self.test_dataset = 0
            self.n=0
            self.k=0
            self.publish = 0
        else:
            self.testSet = {}
            self.test_dataset = 0
            self.label=0
            self.predictions= {}
            self.counter= 0
            self.sign= 0
            self.n=0
            self.k=0
            self.flag = 2
            self.publish = 1

            
    # overloaded
    def receiveMessage(self, data, rssi):

        """
            This is where mesh messages are received
            :param data:  { "sender":string, "payload": dictionary }
        """
        if data["payload"] == "StartTraining" :
            #print ("StartTraining")
            self.label = self.label+1
            self.radiomap[self.label] = {}
            self.flag = 1
        # When I receive "Start training" a flag informs the crownstone to start constructing their radio maps till a "Stop training" is received.
        if data["payload"] == "StopTraining" :
            #print ("StopTraining")
            self.flag = 0 
        if data["payload"] == "StartLocalizing":
            #print ("StartLocalizing")
            self.flag = 2
        # if data["payload"] == "StopLocalizing":
        #     self.flag = 3
    
        if (self.flag == 1):
            #the radio map of each crownstone contains information-RSSI values received from all crownstones.
            if 'rssi' in data['payload']:
                if data["sender"] not in self.radiomap[self.label]:
                    self.radiomap[self.label][data["sender"]]=[]
                self.radiomap[self.label][data["sender"]].append(data['payload']['rssi'])
                #print ("self.radiomap", self.radiomap)


        if (self.flag == 2 and self.sign == 1 and self.k==0):
            #print ("self.radiomap", self.radiomap)
            if (self.k == 0):
                self.parameters = self.crownParameters(self.radiomap) 
                #print ("self.parameters", self.parameters)    
                #i want to calculate the self.parameters only once
                self.k = 1  
            if 'rssi' in data['payload']:
                if self.counter not in self.testSet:
                    self.testSet[self.counter]={}
                if data["sender"] not in self.testSet[self.counter]:
                    self.testSet[self.counter][data["sender"]]=[]
                self.testSet[self.counter][data["sender"]].append(data['payload']['rssi'])
            self.predictions = self.Predictions(self.parameters, self.test_dataset)
            #print ("predictions of room_label", self.predictions)
            accuracy = self.Accuracy(self.test_dataset, self.predictions)
            #print('Accuracy: ' + repr(accuracy) + '%')
               
        
        # if (self.flag == 3 and self.n == 0) or (self.flag == 4):
        #     self.n=1
        #     self.predictions = self.Predictions(self.parameters, self.test_dataset)
        #     print ("predictions of room_label", self.predictions)
        #     #predictions_norm = self.Predictions_norm(self.parameters, self.test_dataset)
        #     #print ("normalized predictions of room_label", self.predictions_norm)
        #     #accuracy = self.Accuracy(self.test_dataset, self.predictions)
        #     #print('Accuracy: ' + repr(accuracy) + '%')
        #     #norm_accuracy = self.Accuracy(self.test_dataset, predictions_norm)
        #     #print('Norm_Accuracy: ' + repr(norm_accuracy) + '%')



    # overloaded
    def newMeasurement(self, data, rssi):
        self.sendMessage({"rssi":rssi})
        if (self.flag == 1):
            if self.id not in self.radiomap[self.label]:
                self.radiomap[self.label][self.id]=[]
            self.radiomap[self.label][self.id].append(rssi)
            #print ("self.radiomap", self.radiomap)

        if (self.flag == 2):
            self.counter = self.counter + 1
            self.sign = 1
            if self.counter not in self.testSet:
                self.testSet[self.counter]={}
            if self.id not in self.testSet[self.counter]:
                self.testSet[self.counter][self.id]=[]
            self.testSet[self.counter][self.id].append(rssi)



    def crownParameters(self, radiomap):
        parameters={}
        for self.label, crowns in self.radiomap.items():
            if self.label not in parameters:
                parameters[self.label]={}
            sorted_crowns = sorted(crowns.items(), key=operator.itemgetter(0))
            for crown, RSSI in sorted_crowns:
                if len(RSSI)!=1 :
                    if crown not in parameters[self.label]:
                        parameters[self.label][crown]=[]
                        parameters[self.label][crown]= self.Statistics(RSSI)
        return parameters


    def Statistics(self, RSSI):
        parameters = [self.MeanValue(RSSI), self.StandardDeviation(RSSI)]
        return parameters


    def MeanValue(self, rss):
        mean = sum(rss)/float(len(rss))
        return mean 


    def StandardDeviation(self, rss):
        average = self.MeanValue(rss)
        variance = sum([pow(RSSI-average,2) for RSSI in rss])/float(len(rss)-1)
        standarddev = math.sqrt(variance)
        return standarddev


    def Predictions(self, parameters, testSet):
        predictions = []
        for counter in self.testSet:
            room_label = self.PredictRoom(self.parameters, self.testSet[counter])
            if self.publish==1:
                if room_label==1:
                    self.publishResult("Room 1")
                elif room_label==2:
                    self.publishResult("Room 2")
                elif room_label==3:
                    self.publishResult("Room 3")
                elif room_label==4:
                    self.publishResult("Room 4")
                elif room_label==5:
                    self.publishResult("Room 5")    
            predictions.append(room_label)
        return predictions


    def Predictions_norm(self, parameters, testSet):
        predictions = []
        for counter in self.testSet:
            room_label = self.PredictRoom_norm(self.parameters, self.testSet[counter])
            self.publishResult(room_label)
            predictions.append(room_label)
        return predictions


    def PredictRoom(self, parameters, testSet):
        probabilities = self.RoomProbabilities(self.parameters, testSet)
        room_predicted, best_probability = None, -1
        for room_label, probability in probabilities.items():
            if room_predicted is None or probability > best_probability:
                best_probability = probability
                room_predicted = room_label
        return room_predicted

    def PredictRoom_norm(self, parameters, testSet):
        probabilities = self.RoomProbabilities_norm(self.parameters, testSet)
        room_predicted, best_probability = None, -1
        for room_label, probability in probabilities.items():
            if room_predicted is None or probability > best_probability:
                best_probability = probability
                room_predicted = room_label
        return room_predicted


    def RoomProbabilities(self, parameters, testSet):
        probabilities={}
        n=0
        for self.label, room_parameters in self.parameters.items():
            probabilities[self.label]=1
            for crown in room_parameters.items():
                for node, rssi in testSet.items():
                    if crown[0] == node:
                        mean=crown[1][0]
                        standardev=crown[1][1]
                        exponent_numerator = math.pow(rssi[0]-mean,2)
                        exponent_denominator = 2*math.pow(standardev,2)
                        exponent_result = math.exp((-exponent_numerator)/exponent_denominator)
                        prob_density = (1 / (math.sqrt(2*math.pi) * standardev)) * exponent_result
                        probabilities[self.label] *= prob_density
                        n=n+1
        #print("probabilities", probabilities)
        return probabilities


    def RoomProbabilities_norm(self, parameters, testSet):
        probabilities1={}
        norm_factor={}
        norm_probabilities={}
        for self.label, room_parameters in self.parameters.items():
            probabilities1[self.label]= {}
            for crown in room_parameters.items():
                if crown[0] not in probabilities1[self.label]:
                    probabilities1[self.label][crown[0]]=[]
                probabilities1[self.label][crown[0]].append(1)
                for node, rssi in testSet.items():
                    if crown[0] == node:
                        mean=crown[1][0]
                        standardev=crown[1][1]
                        exponent_numerator = math.pow(rssi[0]-mean,2)
                        exponent_denominator = 2*math.pow(standardev,2)
                        exponent_result = math.exp((-exponent_numerator)/exponent_denominator)
                        prob_density = (1 / (math.sqrt(2*math.pi) * standardev)) * exponent_result
                        #non-normalized probabilities
                        #product of our prior distribution
                        probabilities1[self.label][node][0] *= prob_density
        #normalization_factor one for each crownstone, sum of non-normalized probabilities for all rooms
        n=1
        for self.label, prob in probabilities1.items():
            for node in prob.items():
                if n <= len(prob):
                    norm_factor[node[0]] = node[1][0]
                    n=n+1
                else:
                    norm_factor[node[0]] += node[1][0]
            #print ("normalization_factor", norm_factor)
        for self.label, prob in probabilities1.items():
            norm_probabilities[self.label]=1
            for node in prob.items():
                norm_probabilities[self.label] *= (1/ norm_factor[node[0]])* node[1][0]
        #print ("norm_probabilities",norm_probabilities)
        return norm_probabilities


    def Accuracy(self, testSet, predictions):
        correct = 0
        room= 3
        for x in range(len(predictions)):
            if room == (predictions[x]):
                correct += 1
        return (correct/float(len(predictions))) * 100.0



##### 1st way : without missing values 

    # the testSet_row for every counter is passed as a list in case there is no missing values.
    #def Predictions(self, parameters, testSet):
    #    predictions = []
    #    for counter in self.testSet:
    #        testList = [self.testSet[counter][key][0] for key in sorted(self.testSet[counter].keys())]
    #        room_label = self.PredictRoom(self.parameters, testList)
    #        predictions.append(room_label)
    #    return predictions

    #In case of not missing values I just regard that each element of a list corresponds to a crownstone/node.
    #def RoomProbabilities_1(self, parameters, testSet):
    #    probabilities={}
    #    for self.label, room_parameters in self.parameters.items():
    #        probabilities[self.label] = 1
    #        for crown in room_parameters.items():
    #            mean=crown[1][0]
    #            standardev=crown[1][1] 
    #            i=crown[0]    
    #            exponent_numerator = math.pow(testSet[i-1]-mean,2)
    #            exponent_denominator = 2*math.pow(standardev,2)
    #            exponent_result = math.exp((-exponent_numerator)/exponent_denominator)
    #            prob_density = (1 / (math.sqrt(2*math.pi) * standardev)) * exponent_result
    #            probabilities[self.label] *= prob_density
    #    return probabilities




            