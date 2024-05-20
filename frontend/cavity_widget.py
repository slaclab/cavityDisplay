from dataclasses import dataclass

import numpy as np
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor, QCursor, QFont, QFontMetrics, QPainter, QPen
from pydm import Display, PyDMChannel
from pydm.widgets.drawing import PyDMDrawingPolygon
from qtpy.QtCore import Property as qtProperty, QRect, Qt, Slot

from frontend.cavity_fault_display import CavityFaultDisplay
from lcls_tools.common.frontend.display.util import showDisplay

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


SHAPE_PARAMETER_DICT = {
    0: ShapeParameters(GREEN_FILL_COLOR, BLACK_TEXT_COLOR, 4, 0),
    1: ShapeParameters(YELLOW_FILL_COLOR, BLACK_TEXT_COLOR, 3, 0),
    2: ShapeParameters(RED_FILL_COLOR, BLACK_TEXT_COLOR, 6, 0),
    3: ShapeParameters(PURPLE_FILL_COLOR, BLACK_TEXT_COLOR, 20, 0),
    4: ShapeParameters(GRAY_FILL_COLOR, BLACK_TEXT_COLOR, 10, 0),
    5: ShapeParameters(DARK_GRAY_COLOR, WHITE_TEXT_COLOR, 10, 0),
}


class CavityWidget(PyDMDrawingPolygon):
    pressPos = None
    clicked = pyqtSignal()

    def __init__(self, parent=None, init_channel=None):
        super(CavityWidget, self).__init__(parent, init_channel)
        self._num_points = 4
        self._cavityText = "TEXT"
        self._underline = False
        self._pen = QPen(BLACK_TEXT_COLOR)  # Shape's border color
        self._rotation = 0
        self._brush.setColor(QColor(201, 255, 203))  # Shape's fill color
        self._pen.setWidth(1.0)
        self._severity_channel: PyDMChannel = None
        self._description_channel: PyDMChannel = None
        self.alarmSensitiveBorder = False
        self.alarmSensitiveContent = False
        self._faultDisplay: Display = None
        # self.clicked.connect(self.show_fault_display)
        self.cavityNumber = None
        self.cmName = None
        self.setCursor(QCursor(Qt.PointingHandCursor))

    # def show_fault_display(self):
    #     showDisplay(self.faultDisplay)

    # The following two functions were copy/pasted from stack overflow
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pressPos = event.pos()

    def mouseReleaseEvent(self, event):
        # ensure that the left button was pressed *and* released within the
        # geometry of the widget; if so, emit the signal;
        if (
            self.pressPos is not None
            and event.button() == Qt.LeftButton
            and event.pos() in self.rect()
        ):
            self.clicked.emit()
        self.pressPos = None

    # @property
    # def faultDisplay(self):
    #     if not self._faultDisplay:
    #         self._faultDisplay = CavityFaultDisplay(
    #             cavity_number=self.cavityNumber, cmName=self.cmName
    #         )
    #         self._faultDisplay.setWindowTitle(
    #             f"CM{self.cmName} Cavity {self.cavityNumber} Faults"
    #         )
    #     return self._faultDisplay

    @qtProperty(str)
    def cavityText(self):
        return self._cavityText

    @cavityText.setter
    def cavityText(self, text):
        self._cavityText = text

    @qtProperty(str)
    def description_channel(self):
        return self._description_channel.address

    @description_channel.setter
    def description_channel(self, value: str):
        self._description_channel = PyDMChannel(
            address=value, value_slot=self.description_changed
        )
        self._description_channel.connect()

    @Slot(np.ndarray)
    def description_changed(self, value: np.ndarray):
        try:
            desc = "".join(chr(i) for i in value)
            self.setToolTip(desc)
        except TypeError:
            self.setToolTip(value)
        self.update()

    @qtProperty(str)
    def severity_channel(self):
        return self._severity_channel.address

    @severity_channel.setter
    def severity_channel(self, value: str):
        self._severity_channel = PyDMChannel(
            address=value, value_slot=self.severity_channel_value_changed
        )
        self._severity_channel.connect()

    @Slot(int)
    def severity_channel_value_changed(self, value: int):
        self.changeShape(
            SHAPE_PARAMETER_DICT[value]
            if value in SHAPE_PARAMETER_DICT
            else SHAPE_PARAMETER_DICT[3]
        )

    def changeShape(self, shapeParameterObject):
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
