import sys, pygame
import math
import numpy, time
from pygame import gfxdraw


from simulator.core.gui.GuiCore import GuiCore, SimulationEventBus
from simulator.core.gui.SimColorRange import SimColorRange
from simulator.core.gui.SimControlInteraction import SimControlInteraction
from simulator.core.gui.SimInteraction import SimInteraction
from simulator.core.gui.SimMath import SimMath
from simulator.core.gui.SimUserBroadcaster import SimUserBroadcaster
from simulator.core.gui.SimUserMovement import SimUserMovement
from simulator.core.gui.SimOverlays import SimOverlays, OverlayModes
from simulator.core.gui.SimControlPanels import SimControlPanels, ControlModes


class SimulationGui(GuiCore):
    width = 1600
    height = 800
    
    pX = 0
    pY = 0
    scaleFactor = 1
    mapPadding = 10
    mapOffset = None
    mapWidth = None
    mapHeight = None
    
    mapData = None
    crownstones = None
    simulatorCrownstones = None
    simulatorCrownstonesMap = {}
    userData = None
    beacons = None
    rooms = None
    config = None

    userBroadcaster = None
    simulationRunning = False
    simulationStarted = False
    
    
    selectedCrownstone = None
    selectedOverlayMode = OverlayModes.DISABLED
    controlMode = ControlModes.SELECT
    
    state = {}
    
    drawRoomOverlays = True
    drawSourceCrownstones = True
    drawSimulationCrownstones = True
    drawSourceBeacons = True
    drawUserPath = True
    drawUserPathTimes = True
    drawUser = True
    
    simulator = None
    
    def __init__(self, width = 1400, height = 800):
        super().__init__(width, height)
        self.controlInteraction = SimControlInteraction(self)
        self.interaction = SimInteraction(self)
        self.simMath = SimMath(self)
        self.simColorRange = SimColorRange(self)
        self.simOverlays = SimOverlays(self)
        self.simControlPanels = SimControlPanels(self)
        self.simUserMovement = SimUserMovement(self)
        
        self.state["pathDrawing"] = False
        
    
    def loadMap(self, mapData):
        self.mapData = mapData
        
    def loadSimulator(self, simulator):
        self.simulator = simulator
        self.simulator.changeEventBus(SimulationEventBus)
     
    def loadCrownstones(self, crownstones):
        self.crownstones = crownstones

    def loadSimulatorCrownstones(self, simulatorCrownstones):
        self.simulatorCrownstones = simulatorCrownstones
        self.simulatorCrownstonesMap = {}
        for crownstone in self.simulatorCrownstones:
            self.simulatorCrownstonesMap[crownstone.id] = crownstone
            
    def loadUserData(self, userData):
        self.userData = userData
        self.simUserMovement.path = userData["path"]
        
    def loadConfig(self, config):
        self.config = config
     
    def loadBeacons(self, beacons):
        self.beacons = beacons
     
    def loadRooms(self, rooms):
        self.rooms = rooms
        
    def startSimulation(self, duration = None):
        self.userBroadcaster = SimUserBroadcaster(self.userData["address"], self)
        self.userBroadcaster.setBroadcastParameters(intervalMs=self.userData["intervalMs"], payload=self.userData["payload"])
        self.config["userWalkingSpeed"] = self.userData["userWalkingSpeed"]
        
        self.simulator.loadBroadcasters([self.userBroadcaster])
        if duration is None:
            duration = self.config["simulationEndTimeS"]
        self.simulator.start(duration)
        self.simulationStarted = True

    def runSimulation(self):
        if not self.simulationStarted:
            self.startSimulation(0)
        
        self.simulationRunning = True
        
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
            
            if self.simulationRunning:
                time.sleep(0.001)
            else:
                time.sleep(0.01)

            if self.simulationRunning:
                self.simulator.continueSimulation(0.25)
                self.text(screen, "SIMULATION RUNNING", (0,0,0), (20, 20))
                self.text(screen, "T = " + "{:3.2f}".format(self.simulator.t), (0,0,0), (20, 50))
            
            
            
            pygame.display.flip()
            
            # handle interaction events
            self.handleEvents(pygame.event.get())
        
   

    def drawOverview(self, screen):
        # the map area will leave 400 px from the right side available. Draw white background:
        mapSide = 650
    
        mWidth  = self.width  - mapSide - 2 * self.mapPadding
        mHeight = self.height - 2 * self.mapPadding
        
        self.mapWidth = mWidth
        self.mapHeight = mHeight
        
        overviewSurface = pygame.Surface((mWidth, mHeight))
        roomOverviewSurface = pygame.Surface((mWidth, mHeight), pygame.SRCALPHA)
        overviewSurface.fill((255, 255, 255, 255))
        drawnSimOverlay = self.simOverlays.draw(overviewSurface, mWidth, mHeight)
        
        if self.drawRoomOverlays:
            self.drawRooms(roomOverviewSurface, mWidth, mHeight)
            overviewSurface.blit(roomOverviewSurface,(0,0))
        self.drawMap(overviewSurface,mWidth,mHeight)
        
        if self.drawSourceCrownstones:
            self.drawCrownstones(overviewSurface, (self.mapPadding, self.mapPadding))
            
        if self.drawSimulationCrownstones:
            self.drawSimCrownstones(overviewSurface, (self.mapPadding, self.mapPadding))
            
        if self.drawSourceBeacons:
            self.drawBeacons(overviewSurface, (self.mapPadding, self.mapPadding))
        
        if self.drawUserPath:
            self.drawPath(overviewSurface)
        
        screen.blit(overviewSurface, (self.mapPadding, self.mapPadding))
        
        return drawnSimOverlay
        
    def drawPath(self, surf):
        lastPos = None
        lastPathPoint = None
        pathTime = 0
        userSpeed = self.config["userWalkingSpeed"]
        pointCount = len(self.simUserMovement.path)
        if pointCount > 0:
            colorStart = (180,180,180)
            
            counter = 0
            
            for pathPoint in self.simUserMovement.path:
                pos = self.xyMetersToPixels(pathPoint)
                if lastPos is not None:
                    color = self._getColor(colorStart, counter, pointCount)
                    pygame.draw.line(surf,color,lastPos,pos,2)
                    dx = pathPoint[0] - lastPathPoint[0]
                    dy = pathPoint[1] - lastPathPoint[1]
                    distance = math.sqrt(dx**2 + dy**2)
                    dt = distance / userSpeed
                    pathTime += dt
                    if pointCount - counter < 5 and self.drawUserPathTimes:
                        self.text(surf, "{:3.1f}".format(pathTime) + 's', color, pos, True)
                lastPos = pos
                lastPathPoint = pathPoint
                counter += 1

            counter = 0
            for pathPoint in self.simUserMovement.path:
                pos = self.xyMetersToPixels(pathPoint)
                self.drawAaCircle(surf, pos,3,self._getColor(colorStart, counter, pointCount))
                counter += 1
                
        if self.userBroadcaster is not None and self.drawUser:
            pos = self.xyMetersToPixels(self.userBroadcaster.pos)
            self.drawAaCircle(surf, pos, 5, (0,62,82))
            
                
    def _getColor(self, startColor, counter, total):
        sc = startColor
        step = 5
        
        if sc[0] > counter*step:
            return sc[0] - counter*step, sc[1], sc[2]
        elif sc[1] > (counter*step - sc[0]):
            return 0, sc[1] - (counter*step - sc[0]), sc[2]
        elif sc[2] > (counter*step - sc[0] - sc[1]):
            return 0, 0, sc[2] - (counter*step - sc[0] - sc[1])
        else:
            return 0,0,0
       
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
            self.drawAaCircle(surf, zeroPos, 8, (255, 0, 0))

    def drawCrownstones(self, surf, offset):
        for crownstone in self.crownstones:
            posInM = (self.mapData["zeroPoint"][0] + crownstone["x"], self.mapData["zeroPoint"][1] + crownstone["y"])
            
            pos = self.xyMetersToPixels(posInM)
            
            cid = crownstone["id"]
            # lambda cid=cid: func(cid) is used to lock the value of cid in this loop to the lambda function.
            self.createClickableCircle(pos, 10, lambda cid=cid: self.interaction.handleCrownstoneClick(cid), offset)
            self.drawAaCircle(surf, pos, 10, (255, 0, 255))

    def drawSimCrownstones(self, surf, offset):
        if self.simulatorCrownstones is None:
            return
        
        for crownstone in self.simulatorCrownstones:
            posInM = (self.mapData["zeroPoint"][0] + crownstone.pos[0], self.mapData["zeroPoint"][1] + crownstone.pos[1])
        
            pos = self.xyMetersToPixels(posInM)
        
            cid = crownstone.id
            # lambda cid=cid: func(cid) is used to lock the value of cid in this loop to the lambda function.
            self.createClickableCircle(pos, 10, lambda cid=cid: self.interaction.handleCrownstoneClick(cid), offset)
            self.drawAaCircle(surf, pos, 10, (0, 100, 255))
            
    def drawBeacons(self, surf, offset):
        for beacon in self.beacons:
            posInM = (self.mapData["zeroPoint"][0] + beacon["x"], self.mapData["zeroPoint"][1] + beacon["y"])
            pos = self.xyMetersToPixels(posInM)

            self.drawAaCircle(surf, pos, 5, (0,255,0))
            
    def xyPixelsToMeters(self, posVector):
        """
        Convert a position in pixels relative to the 0,0 of the map vector to x,y in meters relative to x,y of map
        :param posVector:
        :return:
        """
        return ((posVector[0] / self.scaleFactor) - self.pX, (posVector[1] / self.scaleFactor) - self.pY)
    
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
    
    
    