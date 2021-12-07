from PyQt5.QtGui import QColor

greenFillColor = QColor(9,141,0)
        
yellowFillColor = QColor(244,230,67)

redFillColor = QColor(150,0,0)
        
purpleFillColor = QColor(131,61,235)

grayFillColor = QColor(127,127,127)

blackTextColor = QColor(0,0,0)
darkGrayTextColor = QColor(40,40,40)
whiteTextColor = QColor(250,250,250)

darkPurpleColor = QColor(106,102,212)


class ShapeParameters:
    def __init__(self, fillColor, borderColor, numPoints, rotation):
        self.fillColor = fillColor
        self.borderColor = borderColor
        self.numPoints = numPoints
        self.rotation = rotation

shapeParameterDict = {0: ShapeParameters(greenFillColor, greenFillColor,
                                         4, 0),
                      1: ShapeParameters(yellowFillColor, yellowFillColor,
                                         3, 0),
                      2: ShapeParameters(redFillColor, redFillColor,
                                         6, 0),
                      3: ShapeParameters(purpleFillColor, purpleFillColor,
                                         20, 0),
                      4: ShapeParameters(grayFillColor, grayFillColor,
                                         10,0)}
