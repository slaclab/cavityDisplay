from pydm import Display
from cavityWidget import CavityWidget

class TestShape(Display):
    def __init__(self, parent=None, args=None, ui_filename="testShape.ui"):
        super(TestShape, self).__init__(parent=parent, args=args, ui_filename=ui_filename)
        cavityWidget = CavityWidget()
        cavityWidget.cavityText = "new custom text here"
        self.ui.gridLayout.addWidget(cavityWidget)