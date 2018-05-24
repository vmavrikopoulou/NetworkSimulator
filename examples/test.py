# we need to import this in order to be able to import the simulator
# it does not have to do anything other than be imported.
from util import path

from exampleBroadcasters.IBeacon import IBeacon
from exampleCrownstones.SimpleCrownstone import SimpleCrownstone
from examples.exampleInteractionModules.TrainingAndTesting import TrainingAndTesting

from simulator import Simulator

# create a custom interaction module
interactionModule = TrainingAndTesting("Victoria")

# setup custom crownstones
crownstones = [
    SimpleCrownstone("crownstone1"),
    SimpleCrownstone("crownstone2"),
    SimpleCrownstone("crownstone3"),
]

# configure the beacons
beacon1 = IBeacon('ad:be:df:93:de:ee')
beacon2 = IBeacon('ad:be:df:93:de:ee')
beacon3 = IBeacon('ad:be:df:93:de:ee')

beacon1.setBroadcastParameters(intervalMs=400, payload="ibeaconUUID:Major:Minor:1")
beacon2.setBroadcastParameters(intervalMs=400, payload="ibeaconUUID:Major:Minor:2")
beacon3.setBroadcastParameters(intervalMs=400, payload="ibeaconUUID:Major:Minor:3")

beacon1.setTargetParameters({
    "crownstone1": {"mean": -80, "std": 5},
    "crownstone2": {"mean": -70, "std": 3},
    "crownstone3": {"mean": -50, "std": 6},
})

beacon2.setTargetParameters({
    "crownstone1": {"mean": -80, "std": 5},
    "crownstone2": {"mean": -70, "std": 3},
    "crownstone3": {"mean": -50, "std": 6},
})


beacon3.setTargetParameters({
    "crownstone1": {"mean": -80, "std": 5},
    "crownstone2": {"mean": -70, "std": 3},
    "crownstone3": {"mean": -50, "std": 6},
})

beacons = [beacon1, beacon2, beacon3];



# create a simulator
mySimulation = Simulator()

# setup simulation
mySimulation.loadInteractionModule(interactionModule)
mySimulation.loadCrownstones(crownstones)
mySimulation.loadBroadcasters(beacons)

mySimulation.start(10, timeStep=0.01)
