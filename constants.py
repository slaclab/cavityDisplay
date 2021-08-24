from PyQt5.QtGui import QColor
from scLinac import LINACS, Linac, Cavity
from fault import faults, PvInvalid
from epics import PV

greenFillColor = QColor(201,255,203)
neonGreenBorderColor = QColor(46,248,10)
        
yellowFillColor = QColor(255,253,167)
neonYellowBorderColor = QColor(248,228,0)

redFillColor = QColor(255,195,187)
neonRedBorderColor = QColor(255,0,0)
        
purpleFillColor = QColor(209,203,255)
neonPurpleBorderColor = QColor(170,85,255)

class ShapeParameters:
    def __init__(self, fillColor, borderColor, numPoints, rotation):
        self.fillColor = fillColor
        self.borderColor = borderColor
        self.numPoints = numPoints
        self.rotation = rotation

shapeParameterDict = {0: ShapeParameters(greenFillColor, neonGreenBorderColor,
                                         4, 45),
                      1: ShapeParameters(yellowFillColor, neonYellowBorderColor,
                                         4, 0),
                      2: ShapeParameters(redFillColor, neonRedBorderColor,
                                         6, 0),
                      3: ShapeParameters(purpleFillColor, neonPurpleBorderColor,
                                         20, 0)}
                                         
STATUS_SUFFIX = "CUDSTATUS"
SEVERITY_SUFFIX = "CUDSEVR"


class DisplayCavity(Cavity, object):
    def __init__(self, cavityNum, rackObject):
        super(DisplayCavity, self).__init__(cavityNum, rackObject)
        self.statusPV = self.pvPrefix + STATUS_SUFFIX
        self.severityPV = self.pvPrefix + SEVERITY_SUFFIX

    def runThroughFaults(self, caputDict):
        #self.statusPV.put(str(self.number))
        #self.severityPV.put(0)
        
        caputDict.statusNames.append(self.statusPV)
        caputDict.severityNames.append(self.severityPV)
        for fault in faults:
            try:                               
                if fault.isFaulted(self):
                    caputDict.statusValues.append(fault.tlc)
                    caputDict.severityValues.append(fault.severity)
                    #self.statusPV.put(fault.tlc)
                    #self.severityPV.put(fault.severity)
                    break
                caputDict.statusValues.append(str(self.number))
                caputDict.severityValues.append(0)
                #self.statusPV.put(str(self.number))
                #self.severityPV.put(0)
            except PvInvalid as e:
                print(e)
                caputDict.statusValues.append("INV")
                caputDict.severityValues.append(3)
                #self.statusPV.put("INV")
                #self.severityPV.put(3)
                break

DISPLAY_LINACS = []
for name, cryomoduleList in LINACS.items():
    DISPLAY_LINACS.append(Linac(name, cryomoduleList, DisplayCavity))
    


