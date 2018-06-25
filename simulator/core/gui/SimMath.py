import math, numpy

class SimMath:
    
    gui = None
    
    def __init__(self, gui):
        self.gui = gui

    def _getBeaconCrownstoneDistance(self, beacon, crownstone):
        return self._getDistance(beacon, (crownstone["x"], crownstone["y"], crownstone["z"]))

    def _getDistance(self, posDict, sourcePos):
        dx = sourcePos[0] - posDict["x"]
        dy = sourcePos[1] - posDict["y"]
        dz = sourcePos[2] - posDict["z"]
    
        return math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

    def _calcN(self, beacon):
        sumN = 0
        counter = 0.0
        for crownstone in self.gui.crownstones:
            if crownstone["id"] in beacon["transmitting"]:
                distance = self._getBeaconCrownstoneDistance(beacon, crownstone)
                rssiCalibration = self.gui.config["rssiCalibration"]
                if "rssiCalibration" in beacon:
                    rssiCalibration = beacon["rssiCalibration"]
            
                N = (rssiCalibration - beacon["transmitting"][crownstone["id"]]["mean"]) / (10.0 * math.log10(distance))
                sumN += N
                counter += 1.0
    
        if counter > 0:
            return sumN / counter
        else:
            raise Exception("Beacon does can not get N for any Crownstone")


    """
        N values are from the following function:
        RSSI = -10*N*log(d) + A
        where A is the RSSI at 1 meter (rssiCalibration
    """
    def processNValues(self):
        for beacon in self.gui.beacons:
            N = self._calcN(beacon)
            if N is not None:
                beacon["NValue"] = N

    def getStdToCrownstone(self, crownstone, sourcePos):
        distanceSum = 0
        crownstoneId = crownstone["id"]
        for beacon in self.gui.beacons:
            if crownstoneId in beacon["transmitting"]:
                distanceSum += self._getDistance(beacon, sourcePos)
    
        std = 0
        for beacon in self.gui.beacons:
            if crownstoneId in beacon["transmitting"]:
                distance = self._getDistance(beacon, sourcePos)
                factor = (1 - distance / distanceSum)
                if factor == 0:
                    return beacon["transmitting"][crownstoneId]["std"]
                
                std += factor * beacon["transmitting"][crownstoneId]["std"]
        return std


    def getStdToPosition(self, targetPos, sourcePos):
        distanceSum = 0
        stds = []
        for crownstone in self.gui.crownstones:
            std = self.getStdToCrownstone(crownstone, sourcePos)
            stds.append({"pos": (crownstone["x"], crownstone["y"], crownstone["z"]), "value": std})
        
        for std in stds:
            distanceSum += self._getDistance(targetPos, std["pos"])

        std = 0
        for std in stds:
            distance = self._getDistance(targetPos, std["pos"])
            factor = (1 - distance / distanceSum)
            if factor == 0:
                return std["value"]

            std += factor * std["value"]
        return std
    

    def getRssiCalibrationAt(self, sourcePos):
        distanceSum = 0
    
        for beacon in self.gui.beacons:
            distanceSum += self._getDistance(beacon, sourcePos)
    
        rssiCalibrationResult = 0
        for beacon in self.gui.beacons:
            rssiCalibration = self.gui.config["rssiCalibration"]
            if "rssiCalibration" in beacon:
                rssiCalibration = beacon["rssiCalibration"]
        
            distance = self._getDistance(beacon, sourcePos)
            factor = (1 - distance / distanceSum)
            if factor == 0:
                return rssiCalibration
            rssiCalibrationResult += factor * rssiCalibration
    
        return rssiCalibrationResult

    def getNValueAt(self, sourcePos):
        distanceSum = 0
    
        for beacon in self.gui.beacons:
            distanceSum += self._getDistance(beacon, sourcePos)
    
        NValue = 0
        for beacon in self.gui.beacons:
            distance = self._getDistance(beacon, sourcePos)
            if "NValue" not in beacon:
                raise Exception("N value not in beacon. Run _processNValues first.")
            factor = (1 - distance / distanceSum)
            if factor == 0:
                return beacon["NValue"]
            NValue += factor * beacon["NValue"]
    
        return NValue
    

    def getRssiToCrownstone(self, crownstone, sourcePos):
        distance = self._getDistance(crownstone, sourcePos)
        rssiCalibration = self.getRssiCalibrationAt(sourcePos)
        NValue = self.getNValueAt(sourcePos)
        std = self.getStdToCrownstone(crownstone, sourcePos)

        return self._getRSSI(rssiCalibration, NValue, distance, std)


    def getRssiToPosition(self, targetPos, sourcePos):
        """
        Gets the rssi from a source position to a target position.
        Target position is the receiver and source is the broadcaster.
        :param targetPos: (x,y,z) tuple
        :param sourcePos: (x,y,z) tuple
        :return:
        """
        targetPosDict = {"x": targetPos[0], "y": targetPos[1], "z": targetPos[2]}
        
        distance = self._getDistance(targetPosDict, sourcePos)
        rssiCalibration = self.getRssiCalibrationAt(sourcePos)
        NValue = self.getNValueAt(sourcePos)
        std = self.getStdToPosition(targetPosDict, sourcePos)
    
        return self._getRSSI(rssiCalibration, NValue, distance, std)
    
    def _getRSSI(self, calibration, NValue, distance, std):
        rssiMean = calibration - (10 * NValue) * math.log10(distance)
        rssi = numpy.random.normal(rssiMean, std)
        return rssi