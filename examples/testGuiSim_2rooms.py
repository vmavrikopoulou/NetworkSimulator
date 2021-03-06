# we need to import this in order to be able to import the simulator
# it does not have to do anything other than be imported.
from util import path

from examples.vikoData_2rooms.exampleCrownstones.SimulatorCrownstone import SimulatorCrownstone
from examples.vikoData_2rooms.exampleInteractionModules.TrainingAndTesting import TrainingAndTesting
from simulator import SimulationGui, JsonFileStore, Simulator

mapData = JsonFileStore('./vikoData_2rooms/maps/officesExample.json').getData()
config = JsonFileStore('./vikoData_2rooms/maps/config.json').getData()
rooms = JsonFileStore('./vikoData_2rooms/maps/roomOverlay.json').getData()
userModule = JsonFileStore('./vikoData_2rooms/maps/userData.json').getData()

# SimulationCrownstones are not perse real Crownstones. These are points to which the rssi's will be calculated.
# Real Crownstones and beacons are required to get the std and n fields.
# up left (-12, -6)
# up right_1 (-4,-6)
# up right_2 (0, -3)
# down left (-12, 12)
# down right (0, 12)

#First topology !!!
#20 nodes
simulatorCrownstones = [
	SimulatorCrownstone(1, 0, 0), # X, Y positions in meters relative to zeroPoint on Map
	SimulatorCrownstone(2, 6, 0), # X, Y positions in meters relative to zeroPoint on Map
	SimulatorCrownstone(3, 5, 5), # X, Y positions in meters relative to zeroPoint on Map
	SimulatorCrownstone(4, 11, 15),
	SimulatorCrownstone(5, 11, 13),
	SimulatorCrownstone(6, 8 , 11),
	SimulatorCrownstone(3, 9, 14), # 1_st
	SimulatorCrownstone(8, 8, 3),
	SimulatorCrownstone(9, 6, 15),
	SimulatorCrownstone(10, 11, 10),
	SimulatorCrownstone(11, 1, 7),
	SimulatorCrownstone(4, 1, 14), # 2_nd
	SimulatorCrownstone(13, 9, 5),
	SimulatorCrownstone(14, 2, 10),
	SimulatorCrownstone(15, 9, 8),
	SimulatorCrownstone(16, 2 ,4),
	SimulatorCrownstone(2, 6, 7), # 3_rd
	SimulatorCrownstone(18, 4, 13),
	SimulatorCrownstone(1, 3, 1), # 4_th
	SimulatorCrownstone(20, 12, 4)
]

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

# a.startSimulation(130)
# a.run()



#running without gui interaction:
a.initScreen()
a.render(a.screen)
a.calculateGroundTruthMap()
a.getStaticResults(True)


# # print("truth map", a.groundTruthMap)
# # print("result map", a.resultMap)
#
#
# #compare result map with ground Truth map
# d1 = a.groundTruthMap
# d2 = a.resultMap
# counter = 0
# correct = 0
# for k1, v1 in d1.items():
# 	if k1 in d2:
# 		for v2 in d2[k1]:
# 			for ck in v1.keys():
# 				if ck in d2[k1]:
# 					if (d1[k1][ck]!=None):
# 						counter += 1
# 						if (d1[k1][ck] == d2[k1][ck]):
# 							correct += 1
# accuracy = correct/counter * 100
# print('Accuracy: ' + repr(accuracy) + '%')

#create a map where the most accurate prediction among all crownstones will be saved
c_map={}
conf_map={}
for x in range(85, 735, 10):
	c_map[x] = {}
	conf_map[x] = {}
	for y in range(85, 855, 10):
		c_map[x][y] = None
		conf_map[x][y] = None

count = 0
for stone in simulatorCrownstones:
	a.resultMap = stone.Map
	a.render(a.screen)
	#take the drawing of the result map of each crownstone
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

# the accuracy is not exactly the same for all the crownstones because of the radio map. When the radio map is constructed and the training
# phase goes from one label_room to another there are some data that are still to be relayed as far as TTL = 4


# print ("conf_map", conf_map)
# print(simulatorCrownstones[0].Map)
# print (simulatorCrownstones[0].confidence_Map)
#the accuracy regarding the c_map that has all the best predictions of all crownstones
# correct_1 = 0
# d1 = a.groundTruthMap
# d2 = c_map
# counter_1 = 0
# for k1, v1 in d1.items():
# 	if k1 in d2:
# 		for v2 in d2[k1]:
# 			for ck in v1.keys():
# 				if ck in d2[k1]:
# 					if (d1[k1][ck]!= None):
# 						counter_1 += 1
# 						if (d1[k1][ck]==d2[k1][ck] and d2[k1][ck]!=None):
# 							correct_1 += 1
# Accuracy_cmap = correct_1/counter_1 * 100
# #print ("Combined result map", c_map)
# print ('Accuracy_cmap: ' + repr(Accuracy_cmap) + '%')


