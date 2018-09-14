# we need to import this in order to be able to import the simulator
# it does not have to do anything other than be imported.
from util import path

from examples.vikoData_7rooms.exampleCrownstones.SimulatorCrownstone import SimulatorCrownstone
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

# #10 nodes
# simulatorCrownstones = [
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
# 	SimulatorCrownstone(11, 2, 4)
# ]

# #20 nodes
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

a.run()
#a.startSimulation(225)


# # running without gui interaction:
# a.initScreen()
# a.render(a.screen)
# a.calculateGroundTruthMap()
# a.getStaticResults(False)
# #
# # results live in:
# # print("truth map", a.groundTruthMap)
# # print("result map", a.resultMap)


# d1 = a.groundTruthMap
# d2 = a.resultMap
# counter = 0
# correct = 0

# for k1, v1 in d1.items():
# 	if k1 in d2:
# 	 	for v2 in d2[k1]:
# 	 		for ck in v1.keys():
# 	 			if ck in d2[k1]:
# 	 				counter += 1
# 	 				if (d1[k1][ck]==d2[k1][ck]):
# 	 					correct += 1

# print ("counter", counter)
# print ("correct", correct)
# accuracy = correct/counter * 100
# print ('Accuracy: ' + repr(accuracy) + '%')
			

