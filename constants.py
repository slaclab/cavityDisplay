from PyQt5.QtGui import QColor
from scLinac import LINACS, Linac, Cavity

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

DISPLAY_LINACS = []
for name, cryomoduleList in LINACS.items():
    #print(name, cryomoduleList)
    DISPLAY_LINACS.append(Linac(name, cryomoduleList, Cavity))

