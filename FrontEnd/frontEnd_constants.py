from PyQt5.QtGui import QColor

greenFillColor = QColor(201,255,203)
neonGreenBorderColor = QColor(46,248,10)
        
yellowFillColor = QColor(255,253,167)
neonYellowBorderColor = QColor(248,228,0)

redFillColor = QColor(255,195,187)
neonRedBorderColor = QColor(255,0,0)
        
purpleFillColor = QColor(209,203,255)
neonPurpleBorderColor = QColor(170,85,255)

blackTextColor = QColor(0,0,0)
darkGrayTextColor = QColor(40,40,40)
whiteTextColor = QColor(255,255,255)

darkRedColor = QColor(160,15,15)
darkGreenColor = QColor(22,163,14)
darkPurpleColor = QColor(106,102,212)

class ShapeParameters:
    def __init__(self, fillColor, borderColor, numPoints, rotation):
        self.fillColor = fillColor
        self.borderColor = borderColor
        self.numPoints = numPoints
        self.rotation = rotation

shapeParameterDict = {0: ShapeParameters(darkGreenColor, darkGreenColor,
                                         4, 0),
                      1: ShapeParameters(neonYellowBorderColor, neonYellowBorderColor,
                                         3, 0),
                      2: ShapeParameters(darkRedColor, darkRedColor,
                                         6, 0),
                      3: ShapeParameters(darkPurpleColor, darkPurpleColor,
                                         20, 0)}
