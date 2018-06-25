# we need to import this in order to be able to import the simulator
# it does not have to do anything other than be imported.
from util import path

from examples.exampleBroadcasters.SimulatedUser import SimulatedUser
from examples.exampleCrownstones.SimulatorCrownstone import SimulatorCrownstone
from examples.exampleInteractionModules.TrainingAndTesting import TrainingAndTesting
from simulator import SimulationGui, JsonFileStore, Simulator

mapData = JsonFileStore('./maps/officesExample.json').getData()
crownstones = JsonFileStore('./maps/crownstones.json').getData()
beacons = JsonFileStore('./maps/beacons.json').getData()
config = JsonFileStore('./maps/config.json').getData()
rooms = JsonFileStore('./maps/roomOverlay.json').getData()
userModule = JsonFileStore('./maps/userData.json').getData()


# SimulationCrownstones are not perse real Crownstones. These are points to which the rssi's will be calculated.
# Real Crownstones and beacons are required to get the std and n fields.
simulatorCrownstones = [
    SimulatorCrownstone("crownstone1", 0, 12, 0.3), # X, Y, Z positions in meters relative to zeroPoint on Map
    SimulatorCrownstone("crownstone2", -10, 0, 0.3), # X, Y, Z positions in meters relative to zeroPoint on Map
    SimulatorCrownstone("crownstone3", -5, 5, 0.3),  # X, Y, Z positions in meters relative to zeroPoint on Map
]

# create a custom interaction module
interactionModule = TrainingAndTesting("Victoria")

a = SimulationGui()
a.loadMap(mapData)
a.loadCrownstones(crownstones)
a.loadSimulatorCrownstones(simulatorCrownstones)
a.loadUserData(userModule)
a.loadBeacons(beacons)
a.loadConfig(config)
a.loadRooms(rooms)

b = Simulator()
b.loadInteractionModule(interactionModule)
b.loadCrownstones(simulatorCrownstones)
a.loadSimulator(b) # this will load the user module into the simulator as a broadcaster.

a.run()