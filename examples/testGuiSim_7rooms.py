# we need to import this in order to be able to import the simulator
# it does not have to do anything other than be imported.
from util import path

from examples.vikoData_7rooms.exampleCrownstones.SimulatorCrownstone_originalSender import SimulatorCrownstone
from examples.vikoData_7rooms.exampleInteractionModules.TrainingAndTesting import TrainingAndTesting
from simulator import SimulationGui, JsonFileStore, Simulator

#second room layout
mapData = JsonFileStore('./vikoData_7rooms/maps/officesExample.json').getData()
config = JsonFileStore('./vikoData_7rooms/maps/config.json').getData()
rooms = JsonFileStore('./vikoData_7rooms/maps/roomOverlay.json').getData()
userModule = JsonFileStore('./vikoData_7rooms/maps/userData.json').getData()

#7 nodes, 1 per room
simulatorCrownstones = [
	#room7
	SimulatorCrownstone(1, 4, 11),
	#room6
	SimulatorCrownstone(2, 6, 7),
  	#room1
  	SimulatorCrownstone(3, 4, 3),
  	#room3
	SimulatorCrownstone(4, 12, 4),
	#room2
	SimulatorCrownstone(5, 8, 5),
	#room5
	SimulatorCrownstone(6, 12, 8),
	#room4
	SimulatorCrownstone(7, 14, 10),
]

# 11 nodes
# cs1 = SimulatorCrownstone(1, 5, 11)
# cs1.clusterdId = 1
# simulatorCrownstones = [
# 	#cs1,
# 	#room7
# 	SimulatorCrownstone(1, 5, 11),
# 	#room6
# 	SimulatorCrownstone(2, 6, 7),
#   	#room1
#   	SimulatorCrownstone(3, 4, 1),
#   	#room3
# 	SimulatorCrownstone(4, 12, 4),
# 	#room2
# 	SimulatorCrownstone(5, 6, 5),
# 	#room5
# 	SimulatorCrownstone(6, 11, 7),
# 	#room4
# 	SimulatorCrownstone(7, 15, 11),
# 	SimulatorCrownstone(8, 2, 8),
# 	SimulatorCrownstone(9, 15, 1),
# 	SimulatorCrownstone(10, 14, 8),
# 	SimulatorCrownstone(11, 2, 4),
# 	SimulatorCrownstone(12, 9, 8),
#  	SimulatorCrownstone(13, 2, 8),
# ]

# #24 nodes
# simulatorCrownstones = [
# 	SimulatorCrownstone(1, 9, 10), # X, Y positions in meters relative to zeroPoint on Map
# 	SimulatorCrownstone(2, 5, 11), # X, Y positions in meters relative to zeroPoint on Map
# 	SimulatorCrownstone(3, 6, 7), # X, Y positions in meters relative to zeroPoint on Map
#   	SimulatorCrownstone(4, 15, 5),
#   	SimulatorCrownstone(5, 1, 1),
#   	SimulatorCrownstone(6, 4, 2),
#   	SimulatorCrownstone(7, 8, 1),
# 	SimulatorCrownstone(8, 12, 4),
# 	SimulatorCrownstone(9, 16, 1),
# 	SimulatorCrownstone(10, 9, 4),
# 	SimulatorCrownstone(11, 6, 5),
# 	SimulatorCrownstone(12, 9, 8),
# 	SimulatorCrownstone(13, 2, 8),
# 	SimulatorCrownstone(14, 3, 5),
# 	SimulatorCrownstone(15, 1, 11),
# 	SimulatorCrownstone(16, 16, 7),
# 	SimulatorCrownstone(17, 11, 11),
# 	SimulatorCrownstone(18, 11, 7),
# 	SimulatorCrownstone(19, 14, 10),
# 	SimulatorCrownstone(20, 16, 11),
# 	SimulatorCrownstone(21, 13, 8),
# 	SimulatorCrownstone(22, 11, 1),
# 	SimulatorCrownstone(23, 6, 9),
# 	SimulatorCrownstone(24, 1, 5)
# ]


# create a custom interaction module
interactionModule = TrainingAndTesting("Victoria")

a = SimulationGui()
a.loadMap(mapData)
a.loadSimulatorCrownstones(simulatorCrownstones)
a.loadUserData(userModule)
a.loadConfig(config)
a.loadRooms(rooms)

b = Simulator()
b.loadInteractionModule(interactionModule)
b.loadCrownstones(simulatorCrownstones)
b.loadConfig(config)
a.loadSimulator(b) # this will load the user module into the simulator as a broadcaster.


# a.startSimulation(220)
# a.run()


#running without gui interaction:
a.initScreen()
a.render(a.screen)
a.calculateGroundTruthMap()
a.getStaticResults(True)

			

#create a map where the most accurate prediction among all crownstones will be saved
c_map={}
conf_map={}
for x in range (85, 735, 10):
    c_map[x] = {}
    conf_map[x]={}
    for y in range(85, 855, 10):
        c_map[x][y] = None
        conf_map[x][y] = None

count = 0
for stone in simulatorCrownstones:
	a.resultMap = stone.Map
	a.render(a.screen)
	#a.makeScreenshot("cs_" + str(count) + "_ttl_4.png")
	count += 1
	d1 = a.groundTruthMap
	d2 = a.resultMap
	d3 = stone.confidence_Map
	counter = 0
	correct = 0
	for k1, v1 in d1.items():
		if k1 in d2:
		 	for v2 in d2[k1]:
		 		for ck in v1.keys():
		 			if ck in d2[k1]:
		 				#I don't take into account the None labels (where no room corresponds) in the ground truth map
		 				if (d1[k1][ck] != None):
		 					counter += 1
		 					#I compare the label of each result map of every crownstone with the label in ground truth map. I don't take into account the 
		 					#none values where the room is not in the range of crownstone so it cannot make a room prediction.
			 				if (d1[k1][ck]==d2[k1][ck]) and (d2[k1][ck] != None) :
			 					correct += 1
			 					c_map[k1][ck] = d1[k1][ck]
			 					if (conf_map[k1][ck]== None):
			 						conf_map[k1][ck] = d3[k1][ck]
			 					else:
			 						if (conf_map[k1][ck]<d3[k1][ck]):
			 							conf_map[k1][ck] = d3[k1][ck]
	if (correct != 0):	
		accuracy = correct/counter * 100
		print ("cs_" + str(count) + 'Accuracy_total: ' + repr(accuracy) + '%')
#print ("conf_map", conf_map)
# print(simulatorCrownstones[0].Map)
#print (simulatorCrownstones[0].confidence_Map)
# the accuracy regarding the c_map that has all the best predictions of all crownstones
# correct_1 = 0
# d1 = a.groundTruthMap
# d2 = c_map
# counter_1 = 0
# for k1, v1 in d1.items():
# 	if k1 in d2:
# 	 	for v2 in d2[k1]:
# 	 		for ck in v1.keys():
# 	 			if ck in d2[k1]:
# 	 				counter_1 += 1
# 	 				if (d1[k1][ck]==d2[k1][ck]):
# 	 					correct_1 += 1
# accuracy_2 = correct_1/counter_1 * 100
# print ("Combined result map", c_map)
# print ('Accuracy_cmap: ' + repr(accuracy_2) + '%')


# #for nvalue=4.5:
# # 7 crownstones in total, 1 crownstone_per_room, Accuracy_cmap: 94.02564102564102%
# # 11 crownstones in total, Accuracy_cmap: 99.56410256410257%






