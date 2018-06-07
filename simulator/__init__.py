from simulator.core.SimulationCore import SimulationCore
from simulator.core.gui.SimulationGui import SimulationGui
from simulator.util.JsonFileStore import JsonFileStore

class Simulator(SimulationCore):
    """
    This is a wrapper class to expose an API
    """
    
    def __init__(self):
        super().__init__()
