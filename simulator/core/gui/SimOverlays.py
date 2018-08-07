import pygame,math

from enum import Enum

class OverlayModes(Enum):
    DISABLED = "DISABLED"
    RSSI = "RSSI"
    
class SimOverlays:
    
    gui = None
    blockSize = 10
    
    height = 1 #m
    
    def __init__(self, gui):
        self.gui = gui
        
    def draw(self, surface, mWidth, mHeight):
        if self.gui.selectedOverlayMode is None or self.gui.selectedOverlayMode == OverlayModes.DISABLED:
            return False

        if self.gui.selectedCrownstone is None:
            return False
        
        if self.gui.selectedOverlayMode == OverlayModes.RSSI:
            return self.drawRssiOverlay(surface, mWidth, mHeight)
   
            

    def drawRssiOverlay(self, surface, mWidth, mHeight):
        xBlockCount = math.ceil(mWidth/self.blockSize)
        yBlockCount = math.ceil(mHeight/self.blockSize)
        
        maxRSSI = -50
        minRSSI = -98
        
        self.gui.simColorRange.startRange = minRSSI
        self.gui.simColorRange.endRange   = maxRSSI
        
        targetCrownstone = None
        for crownstone in self.gui.simulatorCrownstones:
            if crownstone.id == self.gui.selectedCrownstone:
                targetCrownstone = crownstone
                break
                
        if targetCrownstone is None:
            return
        
        for i in range(0,xBlockCount):
            for j in range(0,yBlockCount):
                x,y  = self.gui.xyPxToZeroRefMeters(0.5*self.blockSize + i*self.blockSize, 0.5*self.blockSize + j*self.blockSize)
                
                rssi = self.gui.simMath.getRssiToCrownstone(targetCrownstone, (x,y))
                if rssi is not None:
                    color = self.gui.simColorRange.getColor(rssi)
                    
                    pygame.draw.rect(surface, color, (i*self.blockSize, j*self.blockSize, self.blockSize, self.blockSize))

        return True

    def drawGroundTruthOverlay(self, surface, mWidth, mHeight):
        xBlockCount = math.ceil(mWidth / self.blockSize)
        yBlockCount = math.ceil(mHeight / self.blockSize)

        if self.gui.rooms is None:
            return

        for i in range(0, xBlockCount):
            for j in range(0, yBlockCount):
               
                for room in self.gui.rooms:
                    convertedPointList = []
                    for corner in room["corners"]:
                        convertedPointList.append(self.gui.xyMetersToPixels(corner))
        
                    x = i*self.blockSize + 0.5*self.blockSize
                    y = j*self.blockSize + 0.5*self.blockSize
                    inRoom = self.gui.simMath.isPointInPath(x,y,convertedPointList)
            
                    if inRoom:
                        pygame.draw.rect(surface, (room["color"][0],room["color"][1],room["color"][2],80), (i * self.blockSize, j * self.blockSize, self.blockSize, self.blockSize))
                        pygame.draw.rect(surface, (0,0,0), (x,y, 1, 1))
    
        return True
                



