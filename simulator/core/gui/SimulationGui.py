import sys, pygame
import math
import numpy, time
from pygame import gfxdraw


from simulator.core.gui.GuiCore import GuiCore, SimulationEventBus
from simulator.core.gui.SimColorRange import SimColorRange
from simulator.core.gui.SimControlInteraction import SimControlInteraction
from simulator.core.gui.SimInteraction import SimInteraction
from simulator.core.gui.SimMath import SimMath
from simulator.core.gui.SimResultBroadcaster import SimResultBroadcaster
from simulator.core.gui.SimUserBroadcaster import SimUserBroadcaster
from simulator.core.gui.SimUserMovement import SimUserMovement
from simulator.core.gui.SimOverlays import SimOverlays, OverlayModes
from simulator.core.gui.SimControlPanels import SimControlPanels, ControlModes
from simulator.topics.Topics import Topics


class SimulationGui(GuiCore):
    
    def __init__(self, width = 1280, height = 700):
        super().__init__(width, height)
        self.width = width
        self.height = height

        self.pX = 0
        self.pY = 0
        self.scaleFactor = 1
        self.mapPadding = 10
        self.mapOffset = None
        self.mapWidth = None
        self.mapHeight = None

        self.mapData = None
        self.simulatorCrownstones = None
        self.simulatorCrownstonesMap = {}
        self.userData = None
        self.rooms = None
        self.config = None

        self.userBroadcaster = None
        self.simulationRunning = False
        self.simulationStarted = False
        self.collectingStaticResults = False

        self.selectedCrownstone = None
        self.selectedOverlayMode = OverlayModes.DISABLED
        self.controlMode = ControlModes.SELECT

        self.drawRoomOverlays = False
        self.drawSimulationCrownstones = True
        self.drawUserPath = True
        self.drawUserPathTimes = True
        self.drawUser = True

        self.screen = None

        self.simulator = None

        self.blockSize = 10

        
        self.state = {}
        self.resultMap = {}
        self.groundTruthMap = {}
        
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
     
    def loadRooms(self, rooms):
        self.rooms = rooms
        
    def startSimulation(self, duration = None):
        # allow for no user
        if self.userData is not None:
            self.userBroadcaster = SimUserBroadcaster(self.userData["address"], self)
            self.userBroadcaster.setBroadcastParameters(intervalMs=self.userData["intervalMs"], payload=self.userData["payload"])
            self.config["userWalkingSpeed"] = self.userData["userWalkingSpeed"]
        
            self.simulator.loadBroadcasters([self.userBroadcaster])
            
            
        if duration is None:
            duration = self.config["simulationPredefinedEndpoint"]
        self.simulator.start(duration, self.config["simulationTimeStepSeconds"])
        self.simulationStarted = True

    def runSimulation(self):
        if not self.simulationStarted:
            self.startSimulation(0)
        
        self.simulationRunning = True
        
    def initScreen(self):
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF, 32)

        # determine the scale of the map, m/pixel
        pX = self.config["viewPaddingMeters"]
        pY = self.config["viewPaddingMeters"]
        width = self.config["viewWidthMeters"] + 2 * self.config["viewPaddingMeters"]
        height = self.config["viewHeightMeters"] + 2 * self.config["viewPaddingMeters"]

        mapSide = 400

        mWidth = self.width - mapSide - 2 * self.mapPadding
        mHeight = self.height - 2 * self.mapPadding

        self.mapWidth = mWidth
        self.mapHeight = mHeight

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

    def run(self):
        self.initScreen()
    
        while 1:
            self.render(self.screen)
            
    def render(self, screen, skipSleep = False):
        self.prepareForRender()
    
        screen.fill((0, 62, 82, 1.0))
    
        drawnSimOverlay = self.drawOverview(screen)
        self.simControlPanels.draw(screen)
        if drawnSimOverlay:
            self.simColorRange.draw(screen, (self.width - 400, 10))
        
        if not skipSleep:
            if self.simulationRunning:
                time.sleep(0.0001)
            else:
                time.sleep(0.01)
        
        if self.simulationRunning:
            self.simulator.continueSimulation(0.25, self.config["simulationTimeStepSeconds"])
            self.text(screen, "SIMULATION RUNNING", (0, 0, 0), (20, 20))
            self.text(screen, "T = " + "{:3.2f}".format(self.simulator.t), (0, 0, 0), (20, 50))
    
        pygame.display.flip()
    
        # handle interaction events
        self.handleEvents(pygame.event.get())
        
   

    def drawOverview(self, screen):
        # the map area will leave 400 px from the right side available. Draw white background:
        overviewSurface = pygame.Surface((self.mapWidth, self.mapHeight))
        roomOverviewSurface = pygame.Surface((self.mapWidth, self.mapHeight), pygame.SRCALPHA)
        overviewSurface.fill((255, 255, 255, 255))
        drawnSimOverlay = self.simOverlays.draw(overviewSurface, self.mapWidth, self.mapHeight)
        
        self.drawResultMap(overviewSurface)
        
        if self.drawRoomOverlays:
            self.drawRooms(roomOverviewSurface)
            overviewSurface.blit(roomOverviewSurface,(0,0))
        self.drawMap(overviewSurface)
        
        if self.drawSimulationCrownstones:
            self.drawSimCrownstones(overviewSurface, (self.mapPadding, self.mapPadding))
            
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
                    color = self._getColor(colorStart, counter)
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
                self.drawAaCircle(surf, pos,3,self._getColor(colorStart, counter))
                counter += 1
                
        if self.userBroadcaster is not None and self.drawUser:
            pos = self.xyMetersToPixels(self.userBroadcaster.pos)
            self.drawAaCircle(surf, pos, 5, (0,62,82))
            
                
    def _getColor(self, startColor, counter):
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
       
    def drawRooms(self, surf):
        if self.rooms is None:
            return
    
        for room in self.rooms:
            convertedPointList = []
            for corner in room["corners"]:
                convertedPointList.append(self.xyMetersToPixels(corner))
            
            pygame.draw.polygon(surf, (room["color"][0],room["color"][1],room["color"][2],120), convertedPointList)
            pygame.draw.polygon(surf, room["color"], convertedPointList, 3)
            
    def drawMap(self, surf):
        # draw map
        
        m = self.mapData
        # draw walls
        if m is not None:
            for wall in m["walls"]:
                start = self.xyMetersToPixels(wall["start"])
                end = self.xyMetersToPixels(wall["end"])
                thickness = round(wall["thickness"]*self.scaleFactor)
                pygame.draw.line(surf, (0, 0, 0), start, end, thickness)
                


    def drawResultMap(self, surf):
        if self.rooms is None:
            return
        
        roomColorMap = {}
        for room in self.rooms:
            roomColorMap[room["id"]] = (room["color"][0],room["color"][1],room["color"][2],70)
        
        for xKey, xValue in self.resultMap.items():
            for yKey, yValue in xValue.items():
                x = xKey - 0.5 * self.blockSize
                y = yKey - 0.5 * self.blockSize
                if yValue is not None:
                    if yValue in roomColorMap:
                        pygame.draw.rect(surf, roomColorMap[yValue], (x, y, self.blockSize, self.blockSize))
                    else:
                        pygame.draw.rect(surf, (255,255,255,80), (x, y, self.blockSize, self.blockSize))
                else:
                    pygame.draw.rect(surf, (0, 0, 0, 50), (x, y, self.blockSize, self.blockSize))


    def drawSimCrownstones(self, surf, offset):
        if self.simulatorCrownstones is None:
            return
        
        for crownstone in self.simulatorCrownstones:
            pos = self.xyMetersToPixels(crownstone.pos)
        
            cid = crownstone.id
            # lambda cid=cid: func(cid) is used to lock the value of cid in this loop to the lambda function.
            self.createClickableCircle(pos, 10, lambda cid=cid: self.interaction.handleCrownstoneClick(cid), offset)
            self.drawAaCircle(surf, pos, 10, (0, 100, 255))
            
            
    def xyPixelsToMeters(self, posVector):
        """
        Convert a position in pixels relative to the 0,0 of the map vector to x,y in meters relative to x,y of map
        :param posVector:
        :return:
        """
        return (posVector[0] / self.scaleFactor) - self.pX, (posVector[1] / self.scaleFactor) - self.pY
    
    def xyMetersToPixels(self, posVector):
        """
        Convert a position in meters relative to the 0,0 of the map to a pixel value
        :param posVector:
        :return:
        """
        return round((posVector[0] + self.pX) * self.scaleFactor), round((posVector[1] + self.pY) * self.scaleFactor)
    
    
    def calculateGroundTruthMap(self):
        self.groundTruthMap = {}

        xBlockCount = math.ceil(self.mapWidth  / self.blockSize)
        yBlockCount = math.ceil(self.mapHeight / self.blockSize)

        if self.rooms is None:
            return

        for i in range(0, xBlockCount):
            x = i * self.blockSize + 0.5 * self.blockSize
            self.groundTruthMap[x] = {}
            for j in range(0, yBlockCount):
                y = j * self.blockSize + 0.5 * self.blockSize
                self.groundTruthMap[x][y] = None
                
                for room in self.rooms:
                    convertedPointList = []
                    for corner in room["corners"]:
                        convertedPointList.append(self.xyMetersToPixels(corner))
            
                    x = i * self.blockSize + 0.5 * self.blockSize
                    y = j * self.blockSize + 0.5 * self.blockSize
                    inRoom = self.simMath.isPointInPath(x, y, convertedPointList)
            
                    if inRoom:
                        self.groundTruthMap[x][y] = room["id"]

        
    def getStaticResults(self, render = True):
        self.calculateGroundTruthMap()
        
        self.collectingStaticResults = True
        
        self.startSimulation(self.config["trainingPhaseDurationSeconds"])
        xBlockCount = math.ceil(self.mapWidth / self.blockSize)
        yBlockCount = math.ceil(self.mapHeight / self.blockSize)
        
        xStart = 0
        yStart = 0
        
        self.resultMap = {}
        
        if self.rooms is None:
            return
    
        counter = 0
        
        for i in range(xStart, xBlockCount):
            x = i * self.blockSize + 0.5 * self.blockSize
            self.resultMap[x] = {}
            for j in range(yStart, yBlockCount):
                y = j * self.blockSize + 0.5 * self.blockSize
                if self.groundTruthMap[x][y] is not None or self.config["simulateOutsideRooms"]:
                    counter += 1

                    for crownstone in self.simulatorCrownstones:
                        crownstone.debugInformation = {"x": x, "y": y}
    
                    self.resultMap[x][y] = None
                    posInMeters = self.xyPixelsToMeters((x,y))
    
                    self.simulator.resetSimulatorForResults()
                    # fake a user at this point
                    resultBroadcaster = SimResultBroadcaster(self.userData["address"], posInMeters, self)
                    resultBroadcaster.setBroadcastParameters(intervalMs=self.userData["intervalMs"], payload=self.userData["payload"])
    
                    self.simulator.loadBroadcasters([resultBroadcaster])

                    def drawResult(roomId):
                        # store results
                        self.resultMap[x][y] = roomId
                        
                    self.simulator.eventBus.subscribe(Topics.gotResult,  lambda data: drawResult(data["roomId"]) )
                    
                    self.simulator.continueSimulation(self.config["simulationForMeasurementResultMaxSeconds"], self.config["simulationTimeStepSeconds"])
                    
                    if render:
                        if counter%15 == 0:
                            self.render(self.screen, True)
                    else:
                        print("PROGRESS", (i*yBlockCount)/(xBlockCount*yBlockCount))


        self.simulator.resetSimulatorForResults()
        self.collectingStaticResults = False
        if render:
            self.render(self.screen, True)
        


    def getSingleStaticResult(self, render = True):
        self.calculateGroundTruthMap()
        
        self.collectingStaticResults = True
        self.startSimulation(self.config["trainingPhaseDurationSeconds"])
        xBlockCount = math.ceil(self.mapWidth / self.blockSize)
        yBlockCount = math.ceil(self.mapHeight / self.blockSize)

        self.resultMap = {}
        
        if self.rooms is None:
            return
        
        
        i = round(0.2*xBlockCount)
        j = round(0.4*yBlockCount)
        
        x = i * self.blockSize + 0.5 * self.blockSize
        self.resultMap[x] = {}
        y = j * self.blockSize + 0.5 * self.blockSize

        self.resultMap[x][y] = None
        posInMeters = self.xyPixelsToMeters((x,y))

        self.simulator.resetSimulatorForResults()
        # fake a user at this point
        resultBroadcaster = SimResultBroadcaster(self.userData["address"], posInMeters, self)
        resultBroadcaster.debug = True
        resultBroadcaster.setBroadcastParameters(intervalMs=self.userData["intervalMs"], payload=self.userData["payload"])

        self.simulator.loadBroadcasters([resultBroadcaster])
        
        def drawResult(roomId):
            # store results
            self.resultMap[x][y] = roomId
            
        self.simulator.eventBus.subscribe(Topics.gotResult, lambda data: drawResult(data["roomId"]) )
        self.simulator.continueSimulation(self.config["simulationForMeasurementResultMaxSeconds"], self.config["simulationTimeStepSeconds"])
        
        if render:
            self.render(self.screen, True)
        else:
            print("PROGRESS",(i*yBlockCount) / (xBlockCount*yBlockCount))


        self.simulator.resetSimulatorForResults()
        self.collectingStaticResults = False
        
        
    def makeScreenshot(self, filename):
        pygame.image.save(self.screen, filename)
    
        

    

        
                
                
                
                
                
                
                
                