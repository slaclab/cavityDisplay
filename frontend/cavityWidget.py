from PyQt5.QtGui import QColor, QFont, QFontMetrics, QPainter, QPen
from pydm.widgets.drawing import PyDMDrawingPolygon
from qtpy.QtCore import Property as qtProperty, QRect, Qt


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
    
    @qtProperty(str)
    def cavityText(self):
        return self._cavityText
    
    @cavityText.setter
    def cavityText(self, text):
        self._cavityText = text
    
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
