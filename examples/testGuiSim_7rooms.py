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


simulatorCrownstones = [
	SimulatorCrownstone(1, 5, 0), # X, Y positions in meters relative to zeroPoint on Map
	SimulatorCrownstone(2, -10, 0), # X, Y positions in meters relative to zeroPoint on Map
	SimulatorCrownstone(3, 5, 5), # X, Y positions in meters relative to zeroPoint on Map
  	SimulatorCrownstone(4, 0, 6),
  	SimulatorCrownstone(5, 0, -6),
  	SimulatorCrownstone(6, -12, -6),
  	SimulatorCrownstone(7, -11, 5),
	SimulatorCrownstone(8, 0, 0),
	SimulatorCrownstone(9, -2, -2),
	SimulatorCrownstone(10, -8, -3),
	SimulatorCrownstone(11, 2, 4),
	SimulatorCrownstone(12, -11, -4),
	SimulatorCrownstone(13, -2, 3),
	SimulatorCrownstone(14, -9, 3),
	SimulatorCrownstone(15, 4, -5),
	SimulatorCrownstone(16, -6, -6),
	SimulatorCrownstone(17, -3, -5),
	SimulatorCrownstone(18, -5, 4),
	SimulatorCrownstone(19, -6, -2),
	SimulatorCrownstone(20, -3, 1)
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

