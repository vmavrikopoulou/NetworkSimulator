# we need to import this in order to be able to import the simulator
# it does not have to do anything other than be imported.
from util import path

from examples.minimalExample.SimulatorCrownstone import SimulatorCrownstone
from simulator import SimulationGui, JsonFileStore, Simulator

config = JsonFileStore('./minimalExample/config.json').getData()
userModule = JsonFileStore('./minimalExample/userData.json').getData()

root = SimulatorCrownstone("crownstone1", 0,   0)
root.root = True
simulatorCrownstones = [
    root,
    SimulatorCrownstone("crownstone2", 5,  3),
    SimulatorCrownstone("crownstone3", 10,  6),
    SimulatorCrownstone("crownstone4", 15,   9),
    SimulatorCrownstone("crownstone5", 15,   13),
]


a = SimulationGui()
a.loadSimulatorCrownstones(simulatorCrownstones)
a.loadConfig(config)

b = Simulator()
b.loadCrownstones(simulatorCrownstones)
b.loadConfig(config)
a.loadSimulator(b) # this will load the user module into the simulator as a broadcaster.

a.run()
a.startSimulation(2)
