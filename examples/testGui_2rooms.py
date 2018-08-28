# we need to import this in order to be able to import the simulator
# it does not have to do anything other than be imported.
from util import path

from examples.vikoData.exampleCrownstones.SimulatorCrownstone import SimulatorCrownstone
from examples.vikoData.exampleInteractionModules.TrainingAndTesting import TrainingAndTesting
from simulator import SimulationGui, JsonFileStore, Simulator


mapData = JsonFileStore('./vikoData/maps_2rooms/officesExample.json').getData()
config = JsonFileStore('./vikoData/maps_2rooms/config.json').getData()
rooms = JsonFileStore('./vikoData/maps_2rooms/roomOverlay.json').getData()
userModule = JsonFileStore('./vikoData/maps_2rooms/userData.json').getData()



# SimulationCrownstones are not perse real Crownstones. These are points to which the rssi's will be calculated.
# Real Crownstones and beacons are required to get the std and n fields.
# up left (-12, -6)
# up right_1 (-4,-6)
# up right_2 (0, -3)
# down left (-12, 12)
# down right (0, 12)

#First topology !!!
simulatorCrownstones = [
	SimulatorCrownstone(1, 0, 10), # X, Y positions in meters relative to zeroPoint on Map
	SimulatorCrownstone(2, -10, 0), # X, Y positions in meters relative to zeroPoint on Map
	SimulatorCrownstone(3, -5, 5), # X, Y positions in meters relative to zeroPoint on Map
	SimulatorCrownstone(4, -2, 3),
	SimulatorCrownstone(5, -6, 7),
	SimulatorCrownstone(6, -4 , -1),
	SimulatorCrownstone(7, -12, 8),
	SimulatorCrownstone(8, -2, -3),
	SimulatorCrownstone(9, -4, -6),
	SimulatorCrownstone(10, -7, -5),
	SimulatorCrownstone(11, 0, 5), 
	SimulatorCrownstone(12, -12, 9),
	SimulatorCrownstone(13, -9, 5), 
	SimulatorCrownstone(14, -2, 10),
	SimulatorCrownstone(15, -9, 8),
	SimulatorCrownstone(16, -10 , -1),
	SimulatorCrownstone(17, -12, 2),
	SimulatorCrownstone(18, -3, 8),
	SimulatorCrownstone(19, -5, 1),
	SimulatorCrownstone(20, -12, -4)
]


# Second topology !!!


# simulatorCrownstones = [
# 	SimulatorCrownstone(1, 5, 0), # X, Y positions in meters relative to zeroPoint on Map
# 	SimulatorCrownstone(2, -10, 0), # X, Y positions in meters relative to zeroPoint on Map
# 	SimulatorCrownstone(3, 5, 5), # X, Y positions in meters relative to zeroPoint on Map
#   	SimulatorCrownstone(4, 0, 6),
#   	SimulatorCrownstone(5, 0, -6),
#   	SimulatorCrownstone(6, -12, -6),
#   	SimulatorCrownstone(7, -11, 5),
# 	SimulatorCrownstone(8, 0, 0),
# 	SimulatorCrownstone(9, -2, -2),
# 	SimulatorCrownstone(10, -8, -3),
# 	SimulatorCrownstone(11, 2, 4),
# 	SimulatorCrownstone(12, -11, -4),
# 	SimulatorCrownstone(13, -2, 3),
# 	SimulatorCrownstone(14, -9, 3),
# 	SimulatorCrownstone(15, 4, -5),
# 	SimulatorCrownstone(16, -6, -6),
# 	SimulatorCrownstone(17, -3, -5),
# 	SimulatorCrownstone(18, -5, 4),
# 	SimulatorCrownstone(19, -6, -2),
# 	SimulatorCrownstone(20, -3, 1)
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
a.startSimulation(130)


# # running without gui interaction:
# a.initScreen()
# a.render(a.screen)
# a.calculateGroundTruthMap()
# a.doSingleStaticRun(False)
# # 
# # results live in:
# #print(a.groundTruthMap)
# print(a.resultMap)

