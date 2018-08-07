import pygame,math

from enum import Enum

from simulator.core.gui.SimOverlays import OverlayModes


class ControlModes(Enum):
    SELECT = "SELECT"
    OVERLAYS = "OVERLAYS"
    USER_MOVEMENT = "USER_MOVEMENT"
    SIMULATOR = "SIMULATOR"
    
class SimControlPanels:
    
    gui = None
    blockSize = 10
    
    height = 1 #m
    
    def __init__(self, gui):
        self.gui = gui
        
    def draw(self, screen):
        if   self.gui.controlMode == ControlModes.SELECT:
            self.drawModeSelector(screen)
        elif self.gui.controlMode == ControlModes.OVERLAYS:
            self.drawOverlayPanel(screen)
        elif self.gui.controlMode == ControlModes.USER_MOVEMENT:
            self.drawUserMovementPanel(screen)
        elif self.gui.controlMode == ControlModes.SIMULATOR:
            self.drawSimulatorPanel(screen)
            
        self.drawViewToggles(screen)
        
        
        
        
    def drawModeSelector(self, screen):
        drawHeight = 10
        self.gui.text(screen, "Select an operation mode", (255, 255, 255), (self.gui.width - 300, drawHeight))
    
        drawHeight += 30
    
        self.gui.createButton(
            screen,
            "Overlay Mode",
            False,
            (self.gui.width - 300, drawHeight),
            self.gui.controlInteraction.controlOverlayMode
        )

        drawHeight += 80

        self.gui.createButton(
            screen,
            "User Movement Mode",
            False,
            (self.gui.width - 300, drawHeight),
            self.gui.controlInteraction.controlUserMovementMode
        )
    
        drawHeight += 80

        self.gui.createButton(
            screen,
            "Simulator Mode",
            False,
            (self.gui.width - 300, drawHeight),
            self.gui.controlInteraction.controlSimulatorMode
        )


        
    def drawSimulatorPanel(self, screen):
        drawHeight = 10
        self.gui.text(screen, "Simulator Mode", (255, 255, 255), (self.gui.width - 300, drawHeight))

        drawHeight += 30

        self.gui.createButton(
            screen,
            "Start Predefined",
            self.gui.state["pathDrawing"] == True,
            (self.gui.width - 300, drawHeight),
            self.gui.controlInteraction.startSimulation
        )

        drawHeight += 60

        self.gui.createButton(
            screen,
            "Simulate 5 seconds",
            False,
            (self.gui.width - 300, drawHeight),
            self.gui.controlInteraction.simulate5Seconds
        )

        drawHeight += 60

        if not self.gui.simulationRunning:
            self.gui.createButton(
                screen,
                "Start live",
                False,
                (self.gui.width - 300, drawHeight),
                self.gui.controlInteraction.runSimulation
            )
        else:
            self.gui.createButton(
                screen,
                "Stop live",
                False,
                (self.gui.width - 300, drawHeight),
                self.gui.controlInteraction.stopSimulation
            )
        

        
        self.drawBackButton(screen)
        
      
        
        
    def drawUserMovementPanel(self, screen):
        drawHeight = 10
        self.gui.text(screen, "User Movement Mode", (255, 255, 255), (self.gui.width - 300, drawHeight))

        drawHeight += 30

        self.gui.createButton(
            screen,
            "Draw Path",
            self.gui.state["pathDrawing"] == True,
            (self.gui.width - 300, drawHeight),
            self.gui.controlInteraction.togglePathDrawing
        )

        drawHeight += 60

        self.gui.createButton(
            screen,
            "Save to file",
            False,
            (self.gui.width - 300, drawHeight),
            self.gui.simUserMovement.saveToFile
        )
        
        self.drawBackButton(screen)
        

    def drawOverlayPanel(self, screen):
        drawHeight = 10
        self.gui.text(screen, "Overlay Mode", (255, 255, 255), (self.gui.width - 300, drawHeight))
    
        drawHeight += 30
    
        self.gui.text(screen, "Selected Crownstone:", (255, 255, 255), (self.gui.width - 300, drawHeight))
        drawHeight += 20
        if self.gui.selectedCrownstone is not None:
            self.gui.text(screen, str(self.gui.selectedCrownstone), (255, 255, 255), (self.gui.width - 250, drawHeight))
            drawHeight += 40
        
            self.gui.createButton(
                screen,
                "Show RSSI",
                self.gui.selectedOverlayMode == OverlayModes.RSSI,
                (self.gui.width - 300, drawHeight),
                self.gui.controlInteraction.toggleRSSIOverlay
            )
            drawHeight += 120
        
            self.gui.createButton(
                screen,
                "Deselect Crownstone",
                False,
                (self.gui.width - 300, drawHeight),
                self.gui.controlInteraction.deselectCrownstone
            )
        else:
            self.gui.text(screen, "None", (255, 255, 255), (self.gui.width - 250, drawHeight))

        self.drawBackButton(screen)
        
        
    def drawBackButton(self, screen):
        self.gui.createButton(
            screen,
            "Back",
            False,
            
            (self.gui.width - 300, self.gui.height - 70),
            self.gui.controlInteraction.controlSelectMode
        )
        

    def drawViewToggles(self,screen):
        drawHeight = self.gui.height - 270
        sideDistance = 650
        self.gui.text(screen, "Draw Options:", (255, 255, 255), (self.gui.width - sideDistance, drawHeight), True)

        drawHeight += 25
        
        self.gui.createSmallButton(
            screen,
            "Room overlays",
            self.gui.drawRoomOverlays,
            (self.gui.width - sideDistance, drawHeight),
            self.gui.controlInteraction.toggleDrawRoomOverlays
        )

        drawHeight += 50

        self.gui.createSmallButton(
            screen,
            "Simulation Crownstones",
            self.gui.drawSimulationCrownstones,
            (self.gui.width - sideDistance, drawHeight),
            self.gui.controlInteraction.toggleDrawSimulationCrownstones
        )

        drawHeight += 50

        self.gui.createSmallButton(
            screen,
            "User Path",
            self.gui.drawUserPath,
            (self.gui.width - sideDistance, drawHeight),
            self.gui.controlInteraction.toggleDrawUserPath
        )
        drawHeight += 50

        self.gui.createSmallButton(
            screen,
            "User Indicator",
            
            self.gui.drawUser,
            (self.gui.width - sideDistance, drawHeight),
            self.gui.controlInteraction.toggleDrawUserPathIndicator
        )
        drawHeight += 50

        self.gui.createSmallButton(
            screen,
            "User Path Times",
            self.gui.drawUserPathTimes,
            (self.gui.width - sideDistance, drawHeight),
            self.gui.controlInteraction.toggleDrawUserPathTimes
        )
    
