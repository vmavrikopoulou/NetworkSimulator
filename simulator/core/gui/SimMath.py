import math, numpy
import random

class SimMath:
    
    gui = None
    
    def __init__(self, gui):
        self.gui = gui

    @staticmethod
    def getDistance(posDict, sourcePos):
        dx = sourcePos[0] - posDict["x"]
        dy = sourcePos[1] - posDict["y"]
    
        return math.sqrt(dx ** 2 + dy ** 2)

    @staticmethod
    def getDistanceBetweenCrownstones(cs1, cs2):
        dx = cs1.pos[0] - cs2.pos[0]
        dy = cs1.pos[1] - cs2.pos[1]
    
        return math.sqrt(dx ** 2 + dy ** 2)

    def getRssiUserToCrownstone(self, crownstonePos, sourcePos):
        distance = SimMath.getDistance({"x":crownstonePos[0], "y": crownstonePos[1]}, sourcePos)
        rssiCalibration = self.gui.config["rssiCalibrationUser"]
        NValue = self.gui.config["nValueUser"]
        return SimMath.getRSSI(rssiCalibration, NValue, distance, self.gui.config["rssiMinimumUser"], self.gui.config["rssiNoiseFactor"])
        # return SimMath.getRSSI(rssiCalibration, NValue, distance, self.gui.config["rssiMinimumUser"], 0)

    def getRssiFromCrownstone(self, crownstone, sourcePos):
        distance = SimMath.getDistance({"x":crownstone.pos[0], "y":crownstone.pos[1]}, sourcePos)
        rssiCalibration = self.gui.config["rssiCalibrationCrownstone"]
        NValue = self.gui.config["nValueCrownstone"]
        return SimMath.getRSSI(rssiCalibration, NValue, distance, self.gui.config["rssiMinimumCrownstone"], self.gui.config["rssiNoiseFactor"])
        # return SimMath.getRSSI(rssiCalibration, NValue, distance, self.gui.config["rssiMinimumCrownstone"], 0)

    def getRssiToPosition(self, targetPos, sourcePos):
        """
        Gets the rssi from a source position to a target position.
        Target position is the receiver and source is the broadcaster.
        :param targetPos: (x,y) tuple
        :param sourcePos: (x,y) tuple
        :return:
        """
        targetPosDict = {"x": targetPos[0], "y": targetPos[1]}
        
        distance = SimMath.getDistance(targetPosDict, sourcePos)
        rssiCalibration = self.gui.config["rssiCalibrationUser"]
        NValue = self.gui.config["nValueUser"]
    
        return SimMath.getRSSI(rssiCalibration, NValue, distance, self.gui.config["rssiMinimumUser"], self.gui.config["rssiNoiseFactor"])
        # return SimMath.getRSSI(rssiCalibration, NValue, distance, self.gui.config["rssiMinimumUser"], 0)
    

    def isPointInPath(self, x, y, poly):
        """
        x, y -- x and y coordinates of point
        poly -- a list of tuples [(x, y), (x, y), ...]
        """
        num = len(poly)
        i = 0
        j = num - 1
        c = False
        for i in range(num):
            if ((poly[i][1] > y) != (poly[j][1] > y)) and \
                    (x < poly[i][0] + (poly[j][0] - poly[i][0]) * (y - poly[i][1]) /
                     (poly[j][1] - poly[i][1])):
                c = not c
            j = i
        return c

    @staticmethod
    def getRSSI(calibration, NValue, distance, minRssi, noiseFactor):
        if distance != 0:
            rssiMean = calibration - (10 * NValue) * math.log10(distance)
        else: 
            rssiMean = -100
        # rssi = numpy.random.normal(rssiMean, std)
        if rssiMean < minRssi:
            return None

        if noiseFactor > 0:
            return random.normalvariate(rssiMean, noiseFactor * rssiMean)
    
        return rssiMean