import pygame,math

from enum import Enum

class OverlayModes(Enum):
    DISABLED = "DISABLED"
    RSSI = "RSSI"
    
class SimOverlays:
    
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
        xBlockCount = math.ceil(mWidth/self.gui.blockSize)
        yBlockCount = math.ceil(mHeight/self.gui.blockSize)
        
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
                x,y  = self.gui.xyPxToZeroRefMeters(0.5*self.gui.blockSize + i*self.gui.blockSize, 0.5*self.gui.blockSize + j*self.gui.blockSize)
                
                rssi = self.gui.simMath.getRssiToCrownstone(targetCrownstone, (x,y))
                if rssi is not None:
                    color = self.gui.simColorRange.getColor(rssi)
                    
                    pygame.draw.rect(surface, color, (i*self.gui.blockSize, j*self.gui.blockSize, self.gui.blockSize, self.gui.blockSize))

        return True

    def drawGroundTruthOverlay(self, surface, mWidth, mHeight):
        xBlockCount = math.ceil(mWidth / self.gui.blockSize)
        yBlockCount = math.ceil(mHeight / self.gui.blockSize)

        if self.gui.rooms is None:
            return

        for i in range(0, xBlockCount):
            for j in range(0, yBlockCount):
               
                for room in self.gui.rooms:
                    convertedPointList = []
                    for corner in room["corners"]:
                        convertedPointList.append(self.gui.xyMetersToPixels(corner))
        
                    x = i*self.gui.blockSize + 0.5*self.gui.blockSize
                    y = j*self.gui.blockSize + 0.5*self.gui.blockSize
                    inRoom = self.gui.simMath.isPointInPath(x,y,convertedPointList)
            
                    if inRoom:
                        pygame.draw.rect(surface, (room["color"][0],room["color"][1],room["color"][2],80), (i * self.gui.blockSize, j * self.gui.blockSize, self.gui.blockSize, self.gui.blockSize))
                        pygame.draw.rect(surface, (0,0,0), (x,y, 1, 1))
    
        return True
                



