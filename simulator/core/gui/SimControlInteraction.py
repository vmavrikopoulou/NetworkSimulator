from simulator.core.gui.SimOverlays import OverlayModes


class SimControlInteraction:
    gui = None
    
    def __init__(self, simulationGui):
        self.gui = simulationGui
        
    def toggleNValueOverlay(self):
        self._toggleOverlay(OverlayModes.NVALUE)
        
    def toggleRSSIOverlay(self):
        self._toggleOverlay(OverlayModes.RSSI)
        
    def toggleSTDOverlay(self):
        self._toggleOverlay(OverlayModes.STD)
        
    def toggleRSSICalibrationOverlay(self):
        self._toggleOverlay(OverlayModes.RSSI_CALIBRATION)
        
    def deselectCrownstone(self):
        self.gui.selectedCrownstone = None
        
    def _toggleOverlay(self, value):
        if self.gui.selectedOverlayMode == value:
            self.gui.selectedOverlayMode = OverlayModes.DISABLED
        else:
            self.gui.selectedOverlayMode = value