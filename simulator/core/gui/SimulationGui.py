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
from simulator.core.gui.SimControlPanels import SimControlPanels, ControlModes


class SimulationGui(GuiCore):
    width = 1600
    height = 800
    
    pX = 0
    pY = 0
    scaleFactor = 1
    
    mapData = None
    crownstones = None
    beacons = None
    rooms = None
    config = None
    
    selectedCrownstone = None
    selectedOverlayMode = OverlayModes.DISABLED
    controlMode = ControlModes.SELECT
    
    state = {}
    
    drawRoomOverlays = True
    drawSourceCrownstones = True
    drawSourceBeacons = True
    drawUserPath = True
    

    def __init__(self, width = 1400, height = 800):
        super().__init__(width, height)
        self.controlInteraction = SimControlInteraction(self)
        self.interaction = SimInteraction(self)
        self.simMath = SimMath(self)
        self.simColorRange = SimColorRange(self)
        self.simOverlays = SimOverlays(self)
        self.simControlPanels = SimControlPanels(self)
        
        self.state["pathDrawing"] = False
        
    
    def loadMap(self, mapData):
        self.mapData = mapData
     
    def loadCrownstones(self, crownstones):
        self.crownstones = crownstones
      
    def loadConfig(self, config):
        self.config = config
     
    def loadBeacons(self, beacons):
        self.beacons = beacons
     
    def loadRooms(self, rooms):
        self.rooms = rooms
    
    def run(self):
        screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF, 32)
    
        self.simMath.processNValues()
    
        while 1:
            self.prepareForRender()
            
            screen.fill((0,62,82,1.0))
        
            drawnSimOverlay = self.drawOverview(screen)
            self.simControlPanels.draw(screen)
            if drawnSimOverlay:
                self.simColorRange.draw(screen,(self.width - 650, 10))
            
            pygame.display.flip()
            
            # handle interaction events
            self.handleEvents(pygame.event.get())
            
            time.sleep(0.01)
            
        
   

    def drawOverview(self, screen):
        # the map area will leave 200 px from the right side available. Draw white background:
        mapPadding = 10
        mapSide    = 650
    
        mWidth  = self.width  - mapSide - 2 * mapPadding
        mHeight = self.height - 2 * mapPadding
        overviewSurface = pygame.Surface((mWidth, mHeight))
        roomOverviewSurface = pygame.Surface((mWidth, mHeight), pygame.SRCALPHA)
        overviewSurface.fill((255, 255, 255, 255))
        drawnSimOverlay = self.simOverlays.draw(overviewSurface, mWidth, mHeight, (mapPadding, mapPadding))
        
        
        if self.drawRoomOverlays:
            self.drawRooms(roomOverviewSurface, mWidth, mHeight)
            overviewSurface.blit(roomOverviewSurface,(0,0))
        self.drawMap(overviewSurface,mWidth,mHeight)
        
        if self.drawSourceCrownstones:
            self.drawCrownstones(overviewSurface,(mapPadding, mapPadding))
            
        if self.drawSourceBeacons:
            self.drawBeacons(overviewSurface, (mapPadding, mapPadding))
        
        screen.blit(overviewSurface, (mapPadding, mapPadding))
        
        return drawnSimOverlay
        
        
    def drawRooms(self, surf, mWidth, mHeight):
        if self.rooms is None:
            return
    
        for room in self.rooms:
            convertedPointList = []
            for corner in room["corners"]:
                convertedPointList.append(self.xyMetersToPixels(corner))
            
            pygame.draw.polygon(surf, (room["color"][0],room["color"][1],room["color"][2],60), convertedPointList)
            pygame.draw.polygon(surf, room["color"], convertedPointList, 3)
            


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
    