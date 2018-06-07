import pygame, math

class SimColorRange:
    blockSize = 10
    
    startRange = 0
    endRange = 10
    stepCount = 10
    
    gui = None
    
    def __init__(self, gui):
        self.gui = gui

    def draw(self, screen, pos):
        rHeight = 0.5 * self.gui.height
        rangeSurface = pygame.Surface((30+ 100, rHeight + 40), pygame.SRCALPHA, 32)
        valueRange = (self.endRange - self.startRange)
    
        blockHeight = round(rHeight / self.stepCount)
        for i in range(0, self.stepCount):
            value = self.startRange + ((valueRange / self.stepCount) * i)
            
            pygame.draw.rect(rangeSurface, self.getColor(value), (0, round(rHeight / self.stepCount) * i + 10, 30, blockHeight))

        for i in range(0, self.stepCount + 3):
            value = self.startRange + ((valueRange / self.stepCount) * i)
            self.gui.text(rangeSurface, "{:3.3f}".format(value), (255, 255, 255), (35, blockHeight * i))
    
        screen.blit(rangeSurface, pos)

    def getColor(self, value):
        valueRange = (self.endRange - self.startRange)
        if valueRange == 0:
            return 255,0,0
        factor = (value - self.startRange) / valueRange
        
        if factor > 1:
            factor = 1
        elif factor < 0:
            factor = 0
        return round(255 * (1 - factor)), 0, round(255 * factor)

