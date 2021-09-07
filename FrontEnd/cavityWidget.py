from pydm.widgets.drawing import PyDMDrawingPolygon
from qtpy.QtCore import Property, Qt
from PyQt5.QtGui import QColor, QPen, QFont


class CavityWidget(PyDMDrawingPolygon):
    def __init__(self, parent=None, init_channel=None):
        super(CavityWidget, self).__init__(parent, init_channel)
        self._num_points = 4
        self._cavityText = "Hi..................quick brown fox"
        self._pen = QPen(Qt.red)
        self._rotation = 45
        self._brush.setColor(QColor(201,255,203))
        
    @Property(str)
    def cavityText(self):
        return self._cavityText
        
    @cavityText.setter
    def cavityText(self, text):
        self._cavityText = text
        self.update()
    
    def draw_item(self, painter):
        super(CavityWidget, self).draw_item(painter)
        x,y = self.get_center()
        painter.setFont(QFont("Arial",30))
        painter.drawText(x,y,self.cavityText)
        self.update()
        