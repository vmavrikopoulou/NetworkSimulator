# Every crownstone creates its ResultMap and no result is published in order to not influence the way that the testdata 
#is created for every crownstone. A confidence Map with the probabilities that correspond to each labelroom

from simulator.simulatorBases.CrownstoneCore import CrownstoneCore
from simulator.simulatorBases.GuiCrownstoneCore import GuiCrownstoneCore
import math
import operator
import string
import numpy


class SimulatorCrownstone(GuiCrownstoneCore):
    
    """
        Class variables are created here.
    """
    #myValue = False

    def __init__(self, id, x, y):
        super().__init__(id=id,x=x,y=y)
        #self.debugPrint = False
        self.flag, self.label, self.param, self.value= 0, 0, 0, 0 
        self.radiomap, self.predictions, self.testSet, self.probabilities, self.predictedroom = {}, {}, {}, {}, {}
        self.w, self.publish, self.resetTrainingData, self.timelimit_1, self.timelimit_2 = 0, 0, 0, 0, 0 
        self.Map, self.confidence_Map = {}, {}
        self.nodes, self.rooms = 7, 7
        self.cluster, self.counter ={}, {}
        self.count = 1

    def print(self, data):
        if self.debugPrint:
            print(data)


    def resetState(self, resetTrainingData):
        #This is an important method to reset any state the Crownstone may have so the simulation can be restarted.
        #If resetTrainingData is False, you should clear all state data except that referring to the training sets.
        if resetTrainingData == True:
            self.flag, self.label = 0, 0
            self.radiomap = {}
            self.w, self.publish, self.timelimit_1, self.timelimit_2 = 0, 0, 0, 0 
            self.nodes, self.rooms = 7, 7
            self.cluster, self.counter, self.parameters ={}, {}, {}
            self.count, self.param = 1, 1
        else:
            self.predictions, self.testSet, self.probabilities, self.predictedroom = {}, {}, {}, {}
            self.publish, self.resetTrainingData, self.param = 1, 1, 1
            self.nodes, self.rooms = 7, 7
            self.cluster, self.counter ={}, {}
            self.count = 1
            self.flag = 2
            self.timelimit_1 = self.time
            self.timelimit_2 = self.time

        # self.print ("resetTrainingData" + str(self.time))


    def tick(self, time):
        if (self.time > self.timelimit_1 + 1 and self.resetTrainingData == 1 and self.w==1) :
            # print ("crownstone", self.id)
            # print ("timelimit_1", self.timelimit_1)
            self.timelimit_1 = self.time
            #after my time limit I compute the average of the received RSSI values for myself and my neighbors.
            new_testSet= {key: self.testSet.get(key, 0)[0] / self.counter.get(key, 0)[0] for key in set(self.testSet) | set(self.counter)}
            #Only nodes that have already scanned the user can participate in the clustering 
            self.Clustering(new_testSet)
            self.count = self.count + 1

        if (self.time > self.timelimit_2 + 2.5 and self.resetTrainingData == 1 and self.w ==1):
            # print ("crownstone", self.id)
            # print("----------timelimit_2", self.timelimit_2)
            self.w = 0
            self.timelimit_2 =self.time
            print ("crownstone", self.id)
            print ("predictedroom", self.predictedroom)
            print ("probabilities", self.probabilities)
            for count, predictions in self.predictedroom.items():
                if len(predictions) > 1:
                    n, k = 0, 0
                    rooms =[]
                    for head, room in predictions.items():
                        if n == 0:
                            room_label = room[0]
                            k = len(predictions)
                            n = 1
                        else:
                            rooms.append(room[0])

                        for i in range (len(rooms)):
                            if room_label == room[i]:
                                n +=1
                        print ("time", self.time)
                        print ("room_label", room_label)
                        print ("rooms", rooms)
                        print ("n",n)
                    if n == k :
                        print ("cluster heads made the same prediction so we can just update our state with the final prediction")
                        if self.publish == 1:
                            if room[0] == 1:
                                self.publishResult("Room 1")
                            elif room[0] == 2:
                                self.publishResult("Room 2")
                            elif room[0] == 3:
                                self.publishResult("Room 3")
                            elif room[0] == 4:
                                self.publishResult("Room 4")
                            elif room[0] == 5:
                                self.publishResult("Room 5")
                            elif room[0] == 6:
                                self.publishResult("Room 6")
                            elif room[0] == 7:
                                self.publishResult("Room 7")
                    else:
                        print ("cluster heads didn't make the same prediction")
                        final_prediction = self.FinalPredictions(self.predictedroom[count], self.probabilities[count])
                        if self.publish == 1:
                            if final_prediction == 1:
                                self.publishResult("Room 1")
                            elif final_prediction == 2:
                                self.publishResult("Room 2")
                            elif final_prediction == 3:
                                self.publishResult("Room 3")
                            elif final_prediction == 4:
                                self.publishResult("Room 4")
                            elif final_prediction == 5:
                                self.publishResult("Room 5")
                            elif final_prediction == 6:
                                self.publishResult("Room 6")
                            elif final_prediction == 7:
                                self.publishResult("Room 7")
                else:
                    print ("only one cluster head")
                    for head, room in predictions.items():
                        room_label = room[0]
                        if self.publish == 1:
                            if room_label == 1:
                                self.publishResult("Room 1")
                            elif room_label == 2:
                                self.publishResult("Room 2")
                            elif room_label == 3:
                                self.publishResult("Room 3")
                            elif room_label == 4:
                                self.publishResult("Room 4")
                            elif room_label == 5:
                                self.publishResult("Room 5")
                            elif room_label == 6:
                                self.publishResult("Room 6")
                            elif room_label == 7:
                                self.publishResult("Room 7")


    def receiveMessage(self, data, rssi):
        if data["payload"] == "StartTraining" :
            self.label = self.label+1
            self.radiomap[self.label] = {}
            self.flag = 1
        # When I receive "Start training" a flag informs the crownstones to start constructing their radio maps.
        if data["payload"] == "StopTraining" :
            self.flag = 0 
        if data["payload"] == "StartLocalizing":
            #the parameters (mean & standard deviation) to be calculated only once. flag: self.param
            self.param = 1
            self.flag = 2
            self.timelimit_1 = self.time
            self.timelimit_2 = self.time

        # both the radio map construction and the testSet construction are held in both receiveMessage and newMeasurement functions
        # as the radio map of each crownstone contains information (RSSI values) received from other crownstones. Either from all the crownstones
        # in the mesh network (all crownstones have the same data - highest ttl - fully connected graph) or from only their neighbours (ttl=1 - not fully connected graph).        
        if (self.flag == 1):
            #Construction of radiomap.
            if 'rssi' in data['payload']:
                if data['payload']['originalSender'] not in self.radiomap[self.label]:
                    self.radiomap[self.label][data['payload']['originalSender']]=[]
                self.radiomap[self.label][data['payload']['originalSender']].append(data['payload']['rssi'])        
                            
        
        if (self.flag == 2):
            if self.param == 1:
                self.parameters = self.crownParameters(self.radiomap)
                self.param = 0

            if 'rssi' in data['payload']:
                if data['payload']['originalSender'] not in self.testSet:
                    self.testSet[data['payload']['originalSender']]=[]
                    self.counter[data['payload']['originalSender']]=[]
                    self.testSet[data['payload']['originalSender']].append(data['payload']['rssi'])
                    self.counter[data['payload']['originalSender']].append(1)
                else:
                    self.testSet[data['payload']['originalSender']][0] += data['payload']['rssi']
                    self.counter[data['payload']['originalSender']][0] += 1


            if 'predictions' in data['payload']:
                if self.count not in self.predictedroom:
                    self.predictedroom[self.count]={}
                if data['payload']['cluster_head'] not in self.predictedroom[self.count]:
                    self.predictedroom[self.count][data['payload']['cluster_head']]=[]
                self.predictedroom[self.count][data['payload']['cluster_head']].append(data['payload']['predictions'])

                if self.count not in self.probabilities:
                    self.probabilities[self.count]={}
                if data['payload']['cluster_head'] not in self.probabilities[self.count]:
                    self.probabilities[self.count][data['payload']['cluster_head']]=[]
                self.probabilities[self.count][data['payload']['cluster_head']].append(data['payload']['probabilities'])
            
       
    def FinalPredictions(self, predictions, probabilities):
        print ("Now I 'll make the final prediction")
        n, norm_fac, max_prob = 0, 0, 0
        room, probab = {}, {}
        for i in range (1,7):
            room[i]=[]
        for head_pred, pred in predictions.items():
            for head_prob, prob in probabilities.items():
                if head_pred == head_prob:
                    for i in range(1, 7):
                        room[i].append(prob[0][i])
            n+=1
        for i in range(1,7):
            for j in range (0,n-1):
                if room[i][j] == 0:
                    room[i][j]= 0.01e-50
                probab[i]= numpy.prod(room[i])        
        for i in probab:
            norm_fac += probab[i]
        for i in probab:
            probab[i]= probab[i]/norm_fac
        for i in probab:
            if probab[i] > max_prob:
                max_prob = probab[i]
                room = i
        print ("final room prediction", room)
        return room


    def Clustering(self, testSet):
        values =[]
        n, value_node = 0, -100
        print ("testSet", testSet)
        #create a list with the RSSI values, we are interested to compare the RSSI of the node itself (the RSSI of the self.id)
        #with the other RSSI values of the list in order to elect the self.id as a cluster head or as a cluster member.
        for node in testSet:
            if self.id == node:
                #the RSSI value of the node itself
                value_node = testSet[node]
            else:
                values.append(testSet[node])
    
        for i in range(len(values)): 
            if value_node > values[i]:
                n = n+1 

        #in order for the node to elect itself as a cluster head it should have the highest RSSI value among all its neighbors.
        if n == len(values):
            #to fix the bag for the testSet for node 6
            cluster_head = self.id
            print ("cluster_head", cluster_head)
        else:
            #otherwise it elects itself as a member and waits for the header to make the calculations
            cluster_member = self.id
            cluster_head = 0
            print ("cluster_member", cluster_member)


        if self.id == cluster_head:
            probabilities = self.RoomProbabilities_norm(self.parameters, testSet)
            predictions = self.PredictRoom_norm(probabilities)
            print ("predictions", predictions)
            self.count = self.count +1
            if self.count not in self.predictedroom:
                self.predictedroom[self.count]={}
            if self.id not in self.predictedroom[self.count]:
                self.predictedroom[self.count][self.id]=[]
            self.predictedroom[self.count][self.id].append(predictions)
            self.count = self.count - 1
            self.sendMessage({"predictions":predictions, "probabilities":probabilities, "cluster_head":self.id }, 10)


    def newMeasurement(self, data, rssi):
        #print(self.time, self.id, "scans", data["address"], " with payload ", data["payload"], " and rssi:", rssi)
        if (self.flag == 1):
            self.sendMessage({"rssi":rssi, "originalSender":self.id}, 1)
            #Construction of radio map
            if self.id not in self.radiomap[self.label]:
                self.radiomap[self.label][self.id]=[]
            self.radiomap[self.label][self.id].append(rssi)

        if (self.flag == 2):
            self.sendMessage({"rssi":rssi, "originalSender":self.id}, 1)
            #If the crownstone is able to scan the user the flag w is set to 1, otherwise it remains 0
            self.w = 1
            # Every time I receive a new RSSI value I added to the previous one. I don't take different test sets but I make a sum of the RSSI values received.
            if self.id not in self.testSet:
                self.testSet[self.id]=[]
                self.counter[self.id]=[]
                self.testSet[self.id].append(rssi)
                self.counter[self.id].append(1)
            else:
                self.testSet[self.id][0] += rssi
                self.counter[self.id][0] += 1


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


    def PredictRoom_norm(self, probabilities):
        room_predicted, best_probability = None, -1
        for room_label, probability in probabilities.items():
            if room_predicted is None or probability > best_probability:
                best_probability = probability
                room_predicted = room_label
        return room_predicted


    def RoomProbabilities_norm(self, parameters, testSet):
        probabilities1={}
        norm_factor={}
        norm_probabilities={}
        for self.label, room_parameters in self.parameters.items():
            probabilities1[self.label]= {}
            for crown in room_parameters.items():
                for node, rssi in testSet.items():
                    if crown[0] == node:
                        if crown[0] not in probabilities1[self.label]:
                            probabilities1[self.label][crown[0]]=[]
                        probabilities1[self.label][crown[0]].append(1/self.nodes)
                        mean=crown[1][0]
                        standardev=crown[1][1]
                        exponent_numerator = math.pow(rssi-mean,2)
                        exponent_denominator = 2*math.pow(standardev,2)
                        exponent_result = math.exp((-exponent_numerator)/exponent_denominator)
                        prob_density = (1 / (math.sqrt(2*math.pi) * standardev)) * exponent_result
                        #non-normalized probabilities
                        #product of our prior distribution
                        probabilities1[self.label][node][0] *= prob_density
        #normalization_factor one for each crownstone, sum of non-normalized probabilities for all rooms
        n, k, h = 0, 0, 0
        nodes =[]
        for self.label, prob in probabilities1.items():
            for node in prob.items():
                node_number = node[0]
                for i in range(len(nodes)):
                    if node_number == nodes[i]:
                        k = 1
                if k == 1:
                    h = 1
                else:
                    h = 0
                k = 0 
                if n<=len(prob) and h == 0:
                    norm_factor[node[0]] = node[1][0]
                    nodes.append(node[0])
                    n=n+1
                    k = 0
                else:
                    norm_factor[node[0]] += node[1][0]
        for self.label, prob in probabilities1.items():
            norm_probabilities[self.label]=1
            for node in prob.items():
                norm_probabilities[self.label] *= (1/ norm_factor[node[0]])* node[1][0]
        return norm_probabilities


    def Accuracy(self, testSet, predictions):
        correct = 0
        room = 5
        for x in range(len(predictions)):
            if room == (predictions[x]):
                correct += 1
        return (correct/float(len(predictions))) * 100.0
