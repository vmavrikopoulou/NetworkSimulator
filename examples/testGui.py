# we need to import this in order to be able to import the simulator
# it does not have to do anything other than be imported.
from util import path

from simulator import SimulationGui, JsonFileStore

mapData = JsonFileStore('./maps/officesExample.json').getData()
crownstones = JsonFileStore('./maps/crownstones.json').getData()
beacons = JsonFileStore('./maps/beacons.json').getData()
config = JsonFileStore('./maps/config.json').getData()

a = SimulationGui()
a.loadMap(mapData)
a.loadCrownstones(crownstones)
a.loadBeacons(beacons)
a.loadConfig(config)
a.run()