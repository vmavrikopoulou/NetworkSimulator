import sys, pygame
import math
import numpy, time
from pygame import gfxdraw

from simulator.core.gui.GuiCore import GuiCore
from simulator.core.gui.SimColorRange import SimColorRange
from simulator.core.gui.SimControlInteraction import SimControlInteraction
from simulator.core.gui.SimInteraction import SimInteraction
from simulator.core.gui.SimMath import SimMath
from simulator.core.gui.SimOverlays import SimOverlays, OverlayModes


class SimulationGui(GuiCore):
    width = 1600
    height = 800
    
    pX = 0
    pY = 0
    scaleFactor = 1
    
    mapData = None
    crownstones = None
    beacons = None
    config = None
    
    selectedCrownstone = None
    selectedOverlayMode = OverlayModes.DISABLED
    

    def __init__(self, width = 1200, height = 800):
        super().__init__(width, height)
        self.controlInteraction = SimControlInteraction(self)
        self.interaction = SimInteraction(self)
        self.simMath = SimMath(self)
        self.simColorRange = SimColorRange(self)
        self.simOverlays = SimOverlays(self)
        
    
    def loadMap(self, mapData):
        self.mapData = mapData
     
    def loadCrownstones(self, crownstones):
        self.crownstones = crownstones
      
    def loadConfig(self, config):
        self.config = config
     
    def loadBeacons(self, beacons):
        self.beacons = beacons
    
    def run(self):
        screen = pygame.display.set_mode((self.width, self.height))
    
        self.simMath.processNValues()
    
        while 1:
            self.prepareForRender()
            
            screen.fill((0,62,82))

            drawnSimOverlay = self.drawOverview(screen)
            self.drawControlPanel(screen)
            if drawnSimOverlay:
                self.simColorRange.draw(screen,(self.width - 490, 10))
            
            pygame.display.flip()
            
            # handle interaction events
            self.handleEvents(pygame.event.get())
            
            time.sleep(0.01)
            
        
    def drawControlPanel(self, screen):
        drawHeight = 10
        self.text(screen, "Options", (255, 255, 255), (self.width - 300, drawHeight))

        drawHeight += 30
        
        self.createButton(
            screen,
            "Show NValues",
            self.selectedOverlayMode == OverlayModes.NVALUE,
            (self.width - 300, drawHeight),
            self.controlInteraction.toggleNValueOverlay
        )

        drawHeight += 60

        self.createButton(
            screen,
            "Show RSSI Calibration",
            self.selectedOverlayMode == OverlayModes.RSSI_CALIBRATION,
            (self.width - 300, drawHeight),
            self.controlInteraction.toggleRSSICalibrationOverlay
        )
        
        drawHeight += 60

        self.text(screen, "Selected Crownstone:", (255, 255, 255), (self.width - 300, drawHeight))
        drawHeight += 20
        if self.selectedCrownstone is not None:
            self.text(screen, str(self.selectedCrownstone), (255, 255, 255), (self.width - 250, drawHeight))
            drawHeight += 40
            self.createButton(
                screen,
                "Show STD",
                self.selectedOverlayMode == OverlayModes.STD,
                (self.width - 300, drawHeight),
                self.controlInteraction.toggleSTDOverlay
            )
            
            drawHeight += 60
            
            self.createButton(
                screen,
                "Show RSSI",
                self.selectedOverlayMode == OverlayModes.RSSI,
                (self.width - 300, drawHeight),
                self.controlInteraction.toggleRSSIOverlay
            )
            drawHeight += 120
            
            self.createButton(
                screen,
                "Deselect Crownstone",
                False,
                (self.width - 300, drawHeight),
                self.controlInteraction.deselectCrownstone
            )
        else:
            self.text(screen, "None", (255, 255, 255), (self.width - 250, drawHeight))
            
        

        

    def drawOverview(self, screen):
        # the map area will leave 200 px from the right side available. Draw white background:
        mapPadding = 10
        mapSide    = 500
    
        mWidth  = self.width  - mapSide - 2 * mapPadding
        mHeight = self.height - 2 * mapPadding
        overviewSurface = pygame.Surface((mWidth, mHeight))

        pygame.draw.rect(overviewSurface, (255, 255, 255), (0, 0, mWidth, mHeight))
        drawnSimOverlay = self.simOverlays.draw(overviewSurface, mWidth, mHeight, (mapPadding, mapPadding))
        
        self.drawMap(overviewSurface,mWidth,mHeight)
        self.drawCrownstones(overviewSurface,(mapPadding, mapPadding))
        self.drawBeacons(overviewSurface, (mapPadding, mapPadding))
        
        screen.blit(overviewSurface, (mapPadding, mapPadding))
        
        return drawnSimOverlay
        

    def drawMap(self, surf, mWidth, mHeight):
        
        
        # draw map
        m = self.mapData
        if m is not None:
            # determine the scale of the map, m/pixel
            pX = m["padding"]
            pY = m["padding"]
            width  = m["width"] + 2 * m["padding"]
            height = m["height"] + 2 * m["padding"]
            
            hf = mHeight / height
            wf = mWidth / width
            
            scaleFactor = wf
            if width * hf < mWidth:
                scaleFactor = hf
                totalWidth = width * hf
                pX += ((mWidth - totalWidth) * 0.5) / scaleFactor
            else:
                totalHeight = height * hf
                pY += ((mHeight - totalHeight) * 0.5) / scaleFactor
            
            self.pX = pX
            self.pY = pY
            self.scaleFactor = scaleFactor
            
            # draw walls
            for wall in m["walls"]:
                start = self.xyMetersToPixels(wall["start"])
                end = self.xyMetersToPixels(wall["end"])
                thickness = round(wall["thickness"]*scaleFactor)
                pygame.draw.line(surf, (0, 0, 0), start, end, thickness)
                
            # draw zero point
            zeroPos = self.xyMetersToPixels(m["zeroPoint"])
            self.drawAaCircle(surf, zeroPos, 10, (255, 0, 0))


    def drawCrownstones(self, screen, offset):
        for crownstone in self.crownstones:
            posInM = (self.mapData["zeroPoint"][0] + crownstone["x"], self.mapData["zeroPoint"][1] + crownstone["y"])
            
            pos = self.xyMetersToPixels(posInM)
            
            cid = crownstone["id"]
            # lambda cid=cid: func(cid) is used to lock the value of cid in this loop to the lambda function.
            self.createClickableCircle(pos, 10, lambda cid=cid: self.interaction.handleCrownstoneClick(cid), offset)
            self.drawAaCircle(screen, pos, 10, (255, 0, 255))
            
    
    def drawBeacons(self, screen, offset):
        for beacon in self.beacons:
            posInM = (self.mapData["zeroPoint"][0] + beacon["x"], self.mapData["zeroPoint"][1] + beacon["y"])
            pos = self.xyMetersToPixels(posInM)

            self.drawAaCircle(screen, pos, 5, (0,255,0))
            
            
    
    def xyMetersToPixels(self, posVector):
        """
        Convert a position in meters relative to the 0,0 of the map to a pixel value
        :param posVector:
        :return:
        """
        return round((posVector[0] + self.pX) * self.scaleFactor), round((posVector[1] + self.pY) * self.scaleFactor)
    
    def xyPxToZeroRefMeters(self, x, y):
        """
        Convert a position in pixels to a position in meters relative to the zero point on the map
        :param posVector:
        :return:
        """
        mX = x / self.scaleFactor - self.pX - self.mapData["zeroPoint"][0]
        mY = y / self.scaleFactor - self.pY - self.mapData["zeroPoint"][1]
        
        return mX, mY
    