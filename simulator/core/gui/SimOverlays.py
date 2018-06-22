import pygame,math

from enum import Enum

class OverlayModes(Enum):
    DISABLED = "DISABLED"
    NVALUE = "NVALUE"
    RSSI = "RSSI"
    RSSI_CALIBRATION = "RSSI_CALIBRATION"
    STD = "STD"
    
class SimOverlays:
    
    gui = None
    blockSize = 10
    
    height = 1 #m
    
    def __init__(self, gui):
        self.gui = gui
        
    def draw(self, surface, mWidth, mHeight, offset):
        if self.gui.selectedOverlayMode is None or self.gui.selectedOverlayMode == OverlayModes.DISABLED:
            return False

        if self.gui.selectedOverlayMode == OverlayModes.NVALUE:
            return self.drawNValueOverlay(surface, mWidth, mHeight, offset)
            
        elif self.gui.selectedOverlayMode == OverlayModes.RSSI_CALIBRATION:
            return self.drawRssiCalibrationOverlay(surface, mWidth, mHeight, offset)
        
        if self.gui.selectedCrownstone is None:
            return False
        
        if self.gui.selectedOverlayMode == OverlayModes.RSSI:
            return self.drawRssiOverlay(surface, mWidth, mHeight, offset)
        elif self.gui.selectedOverlayMode == OverlayModes.STD:
            return self.drawStdOverlay(surface, mWidth, mHeight, offset)
        
            
            
    def drawNValueOverlay(self, surface, mWidth, mHeight, offset):
        xBlockCount = math.ceil(mWidth/self.blockSize)
        yBlockCount = math.ceil(mHeight/self.blockSize)
        
        maxNValue = 0
        minNValue = 10000
        for beacon in self.gui.beacons:
            maxNValue = max(maxNValue, beacon["NValue"])
            minNValue = min(minNValue, beacon["NValue"])
            
        
        self.gui.simColorRange.startRange = minNValue
        self.gui.simColorRange.endRange = maxNValue
        
        
        for i in range(0,xBlockCount):
            for j in range(0,yBlockCount):
                x,y    = self.gui.xyPxToZeroRefMeters(0.5*self.blockSize + i*self.blockSize, 0.5*self.blockSize + j*self.blockSize)
                nValue = self.gui.simMath.getNValueAt(x,y,1)
                color  = self.gui.simColorRange.getColor(nValue)
                
                pygame.draw.rect(surface, color, (i*self.blockSize, j*self.blockSize, self.blockSize, self.blockSize))
                
        return True

    def drawRssiCalibrationOverlay(self, surface, mWidth, mHeight, offset):
        xBlockCount = math.ceil(mWidth / self.blockSize)
        yBlockCount = math.ceil(mHeight / self.blockSize)

        maxCal = -40
        minCal = -80

        self.gui.simColorRange.startRange = minCal
        self.gui.simColorRange.endRange = maxCal

        for i in range(0, xBlockCount):
            for j in range(0, yBlockCount):
                x, y = self.gui.xyPxToZeroRefMeters(0.5 * self.blockSize + i * self.blockSize, 0.5 * self.blockSize + j * self.blockSize)
                nValue = self.gui.simMath.getRssiCalibrationAt(x, y, 1)
                color = self.gui.simColorRange.getColor(nValue)
    
                pygame.draw.rect(surface, color, (i * self.blockSize, j * self.blockSize, self.blockSize, self.blockSize))

        return True

    def drawRssiOverlay(self, surface, mWidth, mHeight, offset):
        xBlockCount = math.ceil(mWidth/self.blockSize)
        yBlockCount = math.ceil(mHeight/self.blockSize)
        
        maxRSSI = -50
        minRSSI = -100
        
        self.gui.simColorRange.startRange = minRSSI
        self.gui.simColorRange.endRange   = maxRSSI
        
        targetCrownstone = None
        for crownstone in self.gui.crownstones:
            if crownstone["id"] == self.gui.selectedCrownstone:
                targetCrownstone = crownstone
                break
                
        if targetCrownstone is None:
            return
        
        for i in range(0,xBlockCount):
            for j in range(0,yBlockCount):
                x,y   = self.gui.xyPxToZeroRefMeters(0.5*self.blockSize + i*self.blockSize, 0.5*self.blockSize + j*self.blockSize)
                
                rssi  = self.gui.simMath.getRssiToCrownstone(targetCrownstone, x,y,1)
                color = self.gui.simColorRange.getColor(rssi)
                
                pygame.draw.rect(surface, color, (i*self.blockSize, j*self.blockSize, self.blockSize, self.blockSize))

        return True
                



    def drawStdOverlay(self, surface, mWidth, mHeight, offset):
        xBlockCount = math.ceil(mWidth / self.blockSize)
        yBlockCount = math.ceil(mHeight / self.blockSize)

        maxSTD = 0
        minSTD = 10000
        for beacon in self.gui.beacons:
            if self.gui.selectedCrownstone in beacon["transmitting"]:
                maxSTD = max(maxSTD, beacon["transmitting"][self.gui.selectedCrownstone]["std"])
                minSTD = min(minSTD, beacon["transmitting"][self.gui.selectedCrownstone]["std"])

        self.gui.simColorRange.startRange = minSTD
        self.gui.simColorRange.endRange = maxSTD
        
        targetCrownstone = None
        for crownstone in self.gui.crownstones:
            if crownstone["id"] == self.gui.selectedCrownstone:
                targetCrownstone = crownstone
                break
    
        if targetCrownstone is None:
            return
    
        for i in range(0, xBlockCount):
            for j in range(0, yBlockCount):
                x, y = self.gui.xyPxToZeroRefMeters(0.5 * self.blockSize + i * self.blockSize,
                                                    0.5 * self.blockSize + j * self.blockSize)
            
                rssi = self.gui.simMath.getStdToCrownstone(targetCrownstone, x, y, 1)
                color = self.gui.simColorRange.getColor(rssi)
            
                pygame.draw.rect(surface, color, (i * self.blockSize, j * self.blockSize, self.blockSize, self.blockSize))

        return True
