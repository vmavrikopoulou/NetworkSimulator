

class SimInteraction:
    gui = None
    
    def __init__(self, simulationGui):
        self.gui = simulationGui
        
    def handleCrownstoneClick(self, crownstoneId):
        self.gui.selectedCrownstone = crownstoneId