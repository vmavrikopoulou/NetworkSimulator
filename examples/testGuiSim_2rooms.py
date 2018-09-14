# we need to import this in order to be able to import the simulator
# it does not have to do anything other than be imported.
from util import path

from examples.vikoData_2rooms.exampleCrownstones.SimulatorCrownstone_totallydistributed import SimulatorCrownstone
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
simulatorCrownstones = [
	#SimulatorCrownstone(1, 0, 0), # X, Y positions in meters relative to zeroPoint on Map
	#SimulatorCrownstone(2, 6, 0), # X, Y positions in meters relative to zeroPoint on Map
	#SimulatorCrownstone(3, 5, 5), # X, Y positions in meters relative to zeroPoint on Map
	#SimulatorCrownstone(4, 11, 15),
	#SimulatorCrownstone(5, 11, 13),
	#SimulatorCrownstone(6, 8 , 11),
	SimulatorCrownstone(3, 9, 14),
	#SimulatorCrownstone(8, 8, 3),
	#SimulatorCrownstone(9, 6, 15),
	#SimulatorCrownstone(10, 11, 10),
	#SimulatorCrownstone(11, 1, 7), 
	SimulatorCrownstone(4, 1, 14),
	#SimulatorCrownstone(13, 9, 5), 
	#SimulatorCrownstone(14, 2, 10),
	#SimulatorCrownstone(15, 9, 8),
	#SimulatorCrownstone(16, 2 ,4),
	SimulatorCrownstone(2, 6, 7),
	#SimulatorCrownstone(18, 4, 13),
	SimulatorCrownstone(1, 3, 1),
	#SimulatorCrownstone(20, 12, 4)
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

a.startSimulation(130)
a.run()


# # running without gui interaction:
# a.initScreen()
# a.render(a.screen)
# a.calculateGroundTruthMap()
# a.doSingleStaticRun(False)
# #
# # results live in:
# #print(a.groundTruthMap)
# print(a.resultMap)

