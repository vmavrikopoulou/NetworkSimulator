import math, numpy

class SimMath:
    
    gui = None
    
    def __init__(self, gui):
        self.gui = gui

    def _getBeaconCrownstoneDistance(self, beacon, crownstone):
        return self._getDistance(beacon, crownstone["x"], crownstone["y"], crownstone["z"])

    def _getDistance(self, posDict, x, y, z):
        dx = x - posDict["x"]
        dy = y - posDict["y"]
        dz = z - posDict["z"]
    
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
        N values are from
        RSSI = -10*N*log(d) + A
        where A is the RSSI at 1 meter (rssiCalibration
    """
    def processNValues(self):
        for beacon in self.gui.beacons:
            N = self._calcN(beacon)
            if N is not None:
                beacon["NValue"] = N

    def getStdToCrownstone(self, crownstone, x, y, z):
        distanceSum = 0
        crownstoneId = crownstone["id"]
        for beacon in self.gui.beacons:
            distanceSum += self._getDistance(beacon, x, y, z)
    
        std = 0
        for beacon in self.gui.beacons:
            distance = self._getDistance(beacon, x, y, z)
            factor = (1 - distance / distanceSum)
            if factor == 0:
                return beacon["transmitting"][crownstoneId]["std"]
            
            std += factor * beacon["transmitting"][crownstoneId]["std"]
        return std

    def getRssiCalibrationAt(self, x, y, z):
        distanceSum = 0
    
        for beacon in self.gui.beacons:
            distanceSum += self._getDistance(beacon, x, y, z)
    
        rssiCalibrationResult = 0
        for beacon in self.gui.beacons:
            rssiCalibration = self.gui.config["rssiCalibration"]
            if "rssiCalibration" in beacon:
                rssiCalibration = beacon["rssiCalibration"]
        
            distance = self._getDistance(beacon, x, y, z)
            factor = (1 - distance / distanceSum)
            if factor == 0:
                return rssiCalibration
            rssiCalibrationResult += factor * rssiCalibration
    
        return rssiCalibrationResult

    def getNValueAt(self, x, y, z):
        distanceSum = 0
    
        for beacon in self.gui.beacons:
            distanceSum += self._getDistance(beacon, x, y, z)
    
        NValue = 0
        for beacon in self.gui.beacons:
            distance = self._getDistance(beacon, x, y, z)
            if "NValue" not in beacon:
                raise Exception("N value not in beacon. Run _processNValues first.")
            factor = (1 - distance / distanceSum)
            if factor == 0:
                return beacon["NValue"]
            NValue += factor * beacon["NValue"]
    
        return NValue

    def getRssiToCrownstone(self, crownstone, x, y, z):
        distance = self._getDistance(crownstone, x, y, z)
        rssiCalibration = self.getRssiCalibrationAt(x, y, z)
        NValue = self.getNValueAt(x, y, z)
        std = self.getStdToCrownstone(crownstone, x, y, z)
    
        rssiMean = rssiCalibration - (10 * NValue) * math.log10(distance)
        rssi = numpy.random.normal(rssiMean, std)
    
        return rssi