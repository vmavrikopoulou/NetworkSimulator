import sys, pygame, time
import math
import numpy
from pygame import gfxdraw


class GuiCore:
    
    clickableAreas = None
    
    mouseDown = False
    timeMouseDown = 0
    
    fonts = {}
    
    def __init__(self, width, height):
        self.width  = width
        self.height = height
        pygame.init()
        pygame.font.init()
        self.fonts["Lato"] = pygame.font.SysFont("Lato", 25)
        self.fonts["LatoSmall"] = pygame.font.SysFont("Lato", 21)
        self.clickableAreas = []
    
    def text(self, surface, text, color, pos, smallText = False):
        if smallText:
            textSurface = self.fonts["LatoSmall"].render(text, True, color)
        else:
            textSurface = self.fonts["Lato"].render(text, True, color)
        surface.blit(textSurface, pos)
        
    def createButton(self, surface, text, state, pos, callback):
        border = 3
        w = 250
        h = 40

        self._createButton(surface, text, state, pos, callback, border, w, h, False)

    def createSmallButton(self, surface, text, state, pos, callback):
        border = 3
        w = 180
        h = 35
        self._createButton(surface, text, state, pos, callback, border, w, h, True)

    def _createButton(self, surface, text, state, pos, callback, border, w, h, smallText):
        textX = pos[0] + border + 10
        textY = pos[1] + border + 0.25 * (h - 2 * border)
        pygame.draw.rect(surface, (255, 255, 255), (pos[0], pos[1], w, h))
        if state:
            pygame.draw.rect(surface, (160, 235, 88),
                             (pos[0] + border, pos[1] + border, w - 2 * border, h - 2 * border))
            self.text(surface, text, (0, 0, 0), (textX, textY), smallText)
        else:
            pygame.draw.rect(surface, (0, 62, 82), (pos[0] + border, pos[1] + border, w - 2 * border, h - 2 * border))
            self.text(surface, text, (255, 255, 255), (textX, textY), smallText)
        self.createClickableArea(pos, w, h, callback)

    def createClickableRect(self, rect, callback, offset = (0,0)):
        self.clickableAreas.append({"callback":callback, "rect": (rect[0] + offset[0], rect[1] + offset[1], rect[2], rect[3])})
        
    
    def createClickableArea(self, pos, width, height, callback, offset = (0,0)):
        self.clickableAreas.append({ "callback":callback, "rect": (pos[0] + offset[0], pos[1] + offset[1], width, height)})

    
    def createClickableCircle(self, pos, r, callback, offset=(0, 0)):
        self.clickableAreas.append({"callback": callback, "rect": (pos[0] + offset[0] - r, pos[1] + offset[1] - r, 2*r, 2*r)})

    
    def prepareForRender(self):
        self.clickableAreas = []
        
    
    def handleEvents(self, events):
        for event in events:
            self._handleKeystrokes(event)
            self._handleMouse(event)
            if event.type == pygame.QUIT: sys.exit()

    
    def _handleKeystrokes(self, event):
        if event.type == 2:  # key press
            if event.key == 27:
                sys.exit()
            else:
                print("unknown keystroke", event.key)

    
    def _handleMouse(self, event):
        if event.type == 5:  # mouse down
            self.mouseDown = True
            self.timeMouseDown = time.time()
            

        elif event.type == 6:  # mouse up
            self.mouseDown = False
            if time.time() - self.timeMouseDown < 0.5:
                # valid click
                for area in self.clickableAreas:
                    if self._posInRegion(event.pos, area["rect"]):
                        area["callback"]()
        
        elif event.type == 4:  # mouse move
            if self.mouseDown:
                self.pressedMouseMove(event.pos)
        
    
    """Overload me"""
    def pressedMouseMove(self,pos):
        pass

    
    
    def _posInRegion(self, pos, rect):
        """
        rect is [0:topx, 1:topy, 2:w, 3:h]
        :return: True/False
        """
        return rect[0] <= pos[0] <= rect[0] + rect[2] and rect[1] <= pos[1] <= rect[1] + rect[3]
    
    
    def drawAaCircle(self, screen, pos, size, color):
        pygame.gfxdraw.filled_circle(screen, pos[0], pos[1], size, color)
        pygame.gfxdraw.aacircle(screen, pos[0], pos[1], size, color)