import pygame, math
from enum import Enum


class ColorSchemes(Enum):
    BLUE_RED = "BLUE_RED"
    BLUE_GREEN_RED = "BLUE_GREEN_RED"
    GRAY_RED = "GRAY_RED"

class SimColorRange:
    blockSize = 10
    
    startRange = 0
    endRange = 10
    stepCount = 10
    
    colorScheme = ColorSchemes.BLUE_RED
    
    gui = None
    
    def __init__(self, gui):
        self.gui = gui

    def draw(self, screen, pos):
        rHeight = 0.5 * self.gui.height
        rangeSurface = pygame.Surface((30+ 100, rHeight + 40), pygame.SRCALPHA, 32)
        valueRange = (self.endRange - self.startRange)
    
        blockHeight = round(rHeight / self.stepCount)
        for i in range(0, self.stepCount):
            j = self.stepCount - 1 - i
            value = self.startRange + ((valueRange / (self.stepCount-1)) * j)
            
            pygame.draw.rect(rangeSurface, self.getColor(value), (0, round(rHeight / self.stepCount) * i + 10, 30, blockHeight))

        for i in range(0, self.stepCount + 3):
            j = self.stepCount - i
            value = self.startRange + ((valueRange / self.stepCount) * j)
            self.gui.text(rangeSurface, "{:3.3f}".format(value), (255, 255, 255), (35, blockHeight * i))
        
        self.gui.createClickableArea(pos, 50, rHeight, self.changeColorScheme)
        
        screen.blit(rangeSurface, pos)

    def getColor(self, value):
        valueRange = (self.endRange - self.startRange)
        if valueRange == 0:
            if self.colorScheme == ColorSchemes.BLUE_RED:
                    return 0, 0, 255
            elif self.colorScheme == ColorSchemes.GRAY_RED:
                    return 0, 90, 90
            elif self.colorScheme == ColorSchemes.BLUE_GREEN_RED:
                    return 0, 0, 255
            else:
                return 0, 255, 0
        
        factor = (value - self.startRange) / valueRange
        
        if factor > 1:
            factor = 1
        elif factor < 0:
            factor = 0
        
        fraction = (factor%(1/self.stepCount))
        if fraction < 0.5/self.stepCount:
            factor = factor - (factor % (1 / self.stepCount))
        else:
            factor = factor - (factor % (1 / self.stepCount)) + 1/self.stepCount
        
        if self.colorScheme == ColorSchemes.BLUE_RED:
            return round(255 * factor), 0, round(255 * (1 - factor))
        elif self.colorScheme == ColorSchemes.GRAY_RED:
            return round(255 * factor),90 * (1-factor),90 * (1-factor)
        elif self.colorScheme == ColorSchemes.BLUE_GREEN_RED:
            if factor < 0.5:
                return 0, round(255 * factor*2), round(255 * (1 - (factor*2)))
            else:
                return round(255 * (factor-0.5)*2), round(255 * (1 - ((factor-0.5)*2))), 0
        else:
            return 0,255,0

    def changeColorScheme(self):
        if self.colorScheme == ColorSchemes.BLUE_RED:
            self.colorScheme = ColorSchemes.BLUE_GREEN_RED
        elif self.colorScheme == ColorSchemes.BLUE_GREEN_RED:
            self.colorScheme = ColorSchemes.GRAY_RED
        else:
            self.colorScheme = ColorSchemes.BLUE_RED