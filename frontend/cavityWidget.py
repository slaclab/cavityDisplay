from dataclasses import dataclass

from PyQt5.QtGui import QColor, QFont, QFontMetrics, QPainter, QPen
from pydm import PyDMChannel
from pydm.widgets.drawing import PyDMDrawingPolygon
from qtpy.QtCore import Property as qtProperty, QRect, Qt, Slot

GREEN_FILL_COLOR = QColor(9, 141, 0)
YELLOW_FILL_COLOR = QColor(244, 230, 67)
RED_FILL_COLOR = QColor(150, 0, 0)
PURPLE_FILL_COLOR = QColor(131, 61, 235)
GRAY_FILL_COLOR = QColor(127, 127, 127)
BLUE_FILL_COLOR = QColor(14, 191, 255)
LIMEGREEN_FILL_COLOR = QColor(92, 253, 92)

BLACK_TEXT_COLOR = QColor(0, 0, 0)
DARK_GRAY_COLOR = QColor(40, 40, 40)
WHITE_TEXT_COLOR = QColor(250, 250, 250)


@dataclass
class ShapeParameters:
    fillColor: QColor
    borderColor: QColor
    numPoints: int
    rotation: float


SHAPE_PARAMETER_DICT = {"NO_ALARM": ShapeParameters(GREEN_FILL_COLOR, GREEN_FILL_COLOR,
                                                    4, 0),
                        "MINOR"   : ShapeParameters(YELLOW_FILL_COLOR, YELLOW_FILL_COLOR,
                                                    3, 0),
                        "MAJOR"   : ShapeParameters(RED_FILL_COLOR, RED_FILL_COLOR,
                                                    6, 0),
                        "INVALID" : ShapeParameters(PURPLE_FILL_COLOR, PURPLE_FILL_COLOR,
                                                    20, 0),
                        "PARKED"  : ShapeParameters(GRAY_FILL_COLOR, GRAY_FILL_COLOR,
                                                    10, 0)}


class CavityWidget(PyDMDrawingPolygon):
    def __init__(self, parent=None, init_channel=None):
        super(CavityWidget, self).__init__(parent, init_channel)
        self._num_points = 4
        self._cavityText = "TEXT"
        self._underline = False
        self._pen = QPen(QColor(46, 248, 10))  # Shape's border color
        self._rotation = 0
        self._brush.setColor(QColor(201, 255, 203))  # Shape's fill color
        self._pen.setWidth(5.0)
        self._severity_channel: PyDMChannel = None
        self.alarmSensitiveBorder = False
        self.alarmSensitiveContent = False
    
    @qtProperty(str)
    def cavityText(self):
        return self._cavityText
    
    @cavityText.setter
    def cavityText(self, text):
        self._cavityText = text
    
    @qtProperty(str)
    def severity_channel(self):
        return self._severity_channel.address
    
    @severity_channel.setter
    def severity_channel(self, value: str):
        self._severity_channel = PyDMChannel(address=value,
                                             value_slot=self.severity_channel_value_changed)
        self._severity_channel.connect()
    
    @Slot(str)
    def severity_channel_value_changed(self, value: str):
        print(f"{self.severity_channel} changed to {value}")
        self.changeShape(SHAPE_PARAMETER_DICT[value]
                         if value in SHAPE_PARAMETER_DICT
                         else SHAPE_PARAMETER_DICT[3])
    
    def changeShape(self, shapeParameterObject):
        print(f"Changing shape using {self.severity_channel}")
        self.brush.setColor(shapeParameterObject.fillColor)
        self.penColor = shapeParameterObject.borderColor
        self.numberOfPoints = shapeParameterObject.numPoints
        self.rotation = shapeParameterObject.rotation
        self.update()
    
    @qtProperty(bool)
    def underline(self):
        return self._underline
    
    @underline.setter
    def underline(self, underline: bool):
        self._underline = underline
    
    def value_changed(self, new_val):
        super(CavityWidget, self).value_changed(new_val)
        self.cavityText = new_val
        self.update()
    
    def draw_item(self, painter: QPainter):
        super(CavityWidget, self).draw_item(painter)
        x, y, w, h = self.get_bounds()
        rect = QRect(x, y, w, h)
        fm = QFontMetrics(painter.font())
        if self._cavityText:
            sx = rect.width() / fm.width(self._cavityText)
            sy = rect.height() / fm.height()
            
            painter.save()
            painter.translate(rect.center())
            painter.scale(sx, sy)
            painter.translate(-rect.center())
            
            # Text color
            pen = QPen(QColor(240, 240, 240))
            pen.setWidth(5.0)
            
            font = QFont()
            font.setUnderline(self._underline)
            painter.setFont(font)
            
            painter.setPen(pen)
            painter.drawText(rect, Qt.AlignCenter, self._cavityText)
            painter.setPen(self._pen)
            painter.restore()
