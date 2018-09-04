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
	#SimulatorCrownstone(1, 9, 10), # X, Y positions in meters relative to zeroPoint on Map
	#room7
	SimulatorCrownstone(1, 5, 11), # X, Y positions in meters relative to zeroPoint on Map
	#room6
	SimulatorCrownstone(2, 6, 7), # X, Y positions in meters relative to zeroPoint on Map
  	#SimulatorCrownstone(4, 15, 5),
  	#SimulatorCrownstone(5, 1, 1),
  	#room1
  	SimulatorCrownstone(3, 4, 2),
  	#SimulatorCrownstone(7, 8, 1),
  	#room3
	SimulatorCrownstone(4, 12, 4),
	#SimulatorCrownstone(4, 16, 1),
	#SimulatorCrownstone(5, 9, 4),
	#room2
	SimulatorCrownstone(5, 6, 5),
	#SimulatorCrownstone(12, 9, 8),
	#SimulatorCrownstone(13, 2, 8),
	#SimulatorCrownstone(14, 3, 5),
	#SimulatorCrownstone(15, 1, 11),
	#SimulatorCrownstone(16, 16, 7),
	#SimulatorCrownstone(17, 11, 11),
	#room5
	SimulatorCrownstone(6, 11, 7),
	#room4
	SimulatorCrownstone(7, 14, 10),
	#SimulatorCrownstone(20, 16, 11),
	#SimulatorCrownstone(21, 13, 8),
	#SimulatorCrownstone(22, 11, 1),
	#SimulatorCrownstone(23, 6, 9),
	#SimulatorCrownstone(24, 1, 5)
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

#a.startSimulation(200)
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

