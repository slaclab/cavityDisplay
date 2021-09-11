from pydm.widgets.drawing import PyDMDrawingPolygon
from qtpy.QtCore import Property, Qt, QRect
from PyQt5.QtGui import QColor, QPen, QFont, QFontMetrics


class CavityWidget(PyDMDrawingPolygon):
    def __init__(self, parent=None, init_channel=None):
        super(CavityWidget, self).__init__(parent, init_channel)
        self._num_points = 4
        self._cavityText = "TLC"
        self._pen = QPen(QColor(46,248,10))
        self._rotation = 0
        self._brush.setColor(QColor(201,255,203))
        self._pen.setWidth(5.0)
        
    @Property(str)
    def cavityText(self):
        return self._cavityText
        
    @cavityText.setter
    def cavityText(self, text):
        self._cavityText = text
        self.update()
    
    def draw_item(self, painter):
        super(CavityWidget, self).draw_item(painter)
        x,y,w,h = self.get_bounds()
        rect = QRect(x,y,w,h)
        fm = QFontMetrics(painter.font())        
        sx = rect.width()/fm.width(self.cavityText)
        sy = rect.height()/fm.height()
        painter.save()
        painter.translate(rect.center())
        painter.scale(sx, sy)
        painter.translate(-rect.center())
        painter.drawText(rect, Qt.AlignCenter, self.cavityText)
        painter.restore()
        self.update()
        