from pydm import Display
from cavityWidget import CavityWidget
from PyQt5.QtGui import QColor, QPen

class TestShape(Display):
    def __init__(self, parent=None, args=None, ui_filename="testShape.ui"):
        super(TestShape, self).__init__(parent=parent, args=args, ui_filename=ui_filename)
        cavityWidget = CavityWidget()
        cavityWidget.cavityText = "TLC"
        # cavityWidget.penColor = QColor(0,0,0)
        self.ui.gridLayout.addWidget(cavityWidget)
        