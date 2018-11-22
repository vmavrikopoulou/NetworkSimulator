from simulator.simulatorBases.CrownstoneCore import CrownstoneCore
from simulator.simulatorBases.GuiCrownstoneCore import GuiCrownstoneCore
import math
import operator
import string
import numpy as np
from scipy.stats import norm
import numpy as np
import numpy

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
        self.w1=0
        self.w2=0
        self.prob1 =0
        self.prob2 =0
        self.prob3 =0
        self.publish=0
        self.probabilities = []
        self.people = {}
        self.room_predicted=[]
        self.dataset=[]
        self.room1, self.room2, self.room3, self.room4, self.room5, self.room6, self.room7 = [], [], [], [], [], [], []

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
            self.w1=0
            self.w2=0
            self.w3=0
            self.prob1 =0
            self.prob2 =0
            self.prob3 =0
            self.publish = 0
            self.probabilities = {}
            self.room_predicted=[]
            self.dataset=[]
        else:
            self.testSet = {}
            self.test_dataset = 0
            self.label=0
            self.predictions= {}
            self.counter= 0
            self.sign= 0
            self.n=0
            self.k=0
            self.w1=0
            self.w2=0
            self.w3=0
            self.prob1 =0
            self.prob2 =0
            self.prob3 =0
            self.flag = 2
            self.publish = 1
            self.probabilities = {}
            self.room_predicted=[]
            self.dataset=[]

            
    # overloaded
    def receiveMessage(self, data, rssi):
        #print ("Crownstone", self.id, "receives from Crownstone", data["sender"], "data", data["payload"], "and rssi", rssi)
        """
            This is where mesh messages are received
            :param data:  { "sender":string, "payload": dictionary }
        """
        if data["payload"] == "StartTraining":
            self.label = self.label+1
            self.radiomap[self.label] = {}
            self.flag = 1
        # When I receive "Start training" a flag informs the crownstone to start constructing their radio maps till a "Stop training" is received.
        if data["payload"] == "StopTraining":
            self.flag = 0 
        if data["payload"] == "StartLocalizing":
            self.flag = 2
            
        if (self.flag == 2) and (self.id == 5):
            #print ("Crownstone", self.id, "receives from Crownstone", data["sender"], "data", data["payload"], "and rssi", rssi)
            if self.w1 % 2 != 0:
                self.room1, self.room2, self.room3, self.room4, self.room5, self.room6, self.room7 = [],[],[],[],[],[],[]
            #print ("selfw1", self.w1)
            if self.w1%2 != 0:
                if self.id in self.probabilities:
                    self.room1.append(self.probabilities[self.id][1])
                    self.room2.append(self.probabilities[self.id][2])
                    self.room3.append(self.probabilities[self.id][3])
                    self.room4.append(self.probabilities[self.id][4])
                    self.room5.append(self.probabilities[self.id][5])
                    self.room6.append(self.probabilities[self.id][6])
                    self.room7.append(self.probabilities[self.id][7])
            for key in data['payload']:
                if (key == 1 or key == 2 or key == 3 or key == 4 or key ==6 or key == 7):
                    self.room1.append(data['payload'][key][1])
                    self.room2.append(data['payload'][key][2])
                    self.room3.append(data['payload'][key][3])
                    self.room4.append(data['payload'][key][4])
                    self.room5.append(data['payload'][key][5])
                    self.room6.append(data['payload'][key][6])
                    self.room7.append(data['payload'][key][7])
                    print ("self.room1", self.room1)
                    if self.w1 % 2 == 0:
                        prob1 = numpy.prod(self.room1) 
                        print ("probability1", prob1) 
                        prob2 = numpy.prod(self.room2) 
                        #print ("probability2", prob2) 
                        prob3 = numpy.prod(self.room3) 
                        #print ("probability3", prob3)
                        prob4 = numpy.prod(self.room4) 
                        #print ("probability4", prob4) 
                        prob5 = numpy.prod(self.room5) 
                        #print ("probability5", prob5) 
                        prob6 = numpy.prod(self.room6) 
                        #print ("probability6", prob6) 
                        prob7 = numpy.prod(self.room7) 
                        #print ("probability7", prob7)
                        a = prob1 + prob2 + prob3 + prob4 + prob5 + prob6 + prob7
                        print ("normalization_factor", a)
                        self.prob1 = prob1/a
                        print ("prob1", self.prob1)
                        self.prob2 = prob2/a
                        #print ("prob2", self.prob2)
                        self.prob3 = prob3/a
                        #print ("prob3", self.prob3)
                        self.prob4 = prob4/a
                        #print ("prob4", self.prob4)
                        self.prob5 = prob5/a
                        #print ("prob5", self.prob5)
                        self.prob6 = prob6/a
                        #print ("prob6", self.prob6)
                        self.prob7 = prob7/a
                        #print ("prob7", self.prob7)
                        best_prob = self.prob1
                        room_pred = 1
                        if self.prob2 > best_prob :
                            best_prob = self.prob2
                            room_pred = 2
                        if self.prob3 > best_prob:
                            best_prob = self.prob3
                            room_pred = 3
                        if self.prob4 > best_prob:
                            best_prob = self.prob4
                            room_pred = 4
                        if self.prob5 > best_prob:
                            best_prob = self.prob5
                            room_pred = 5
                        if self.prob6 > best_prob:
                            best_prob = self.prob6
                            room_pred = 6
                        if self.prob7 > best_prob:
                            best_prob = self.prob7
                            room_pred = 7
                        self.room_predicted.append(room_pred)
            self.w1=self.w1+1
            #print ("room1", self.room1)
            #print ("room2", self.room2)
            #print ("room3", self.room3)
            #print ("room4", self.room4)
            #print ("room5", self.room5)
            #print ("room6", self.room6)
            #print ("room7", self.room7)
            #print ("room_predicted", self.room_predicted)                    
            

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
        if (self.flag == 1):
            if self.id not in self.radiomap[self.label]:
                self.radiomap[self.label][self.id]=[]
            self.radiomap[self.label][self.id].append(rssi)
           
        if (self.flag == 2):
            if (self.k == 0):
                self.parameters = self.crownParameters(self.radiomap)
                self.k = 1 
            self.counter = self.counter + 1
            if self.counter not in self.testSet:
                self.testSet[self.counter]={}
            if self.id not in self.testSet[self.counter]:
                self.testSet[self.counter][self.id]=[]
            self.testSet[self.counter][self.id].append(rssi) 
            if self.w2%10 != 0 :
                #print ("time", self.time)
                self.dataset.append(self.testSet[self.counter][self.id][0])
                self.w2 = self.w2 + 1
                #print ("dataset", self.dataset)
            else:
                dataset_array = np.asarray(self.dataset)
                print ("dataset_array", dataset_array)
                mu, std = norm.fit(dataset_array)
                print ("mean", mu)
                print ("standard deviation", std)
                self.dataset = []
                self.probabilities[self.id]=self.Predictions_norm(self.parameters, self.test_dataset)
                self.sendMessage(self.probabilities, 2)

                self.w2 = self.w2 + 1


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

    def Predictions_norm(self, parameters, testSet):
        for counter in self.testSet:
            probabilities = self.RoomProbabilities_norm(self.parameters, self.testSet[counter])
            #self.publishResult(room_label)
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
        #print ('probabilities1', probabilities1)
        #normalization_factor one for each crownstone, sum of non-normalized probabilities for all rooms
        n=1
        for self.label, prob in probabilities1.items():
            #print ("prob", prob)
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
        #print ('norm_probabilities', norm_probabilities)
        return norm_probabilities

    def Accuracy(self, testSet, predictions):
        correct = 0
        room= 2
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




            