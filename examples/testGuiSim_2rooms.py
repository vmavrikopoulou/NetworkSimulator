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

# a.startSimulation(125)
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

