from PyQt5 import QtCore, QtGui
# from PyQt5.QtGui import QMouseEvent
# from PyQt5.QtCore import Qt
from pydm import Display


# from PyQt5 import QtGui


class Click(Display):
    def __init__(self, parent=None, args=None):
        super().__init__(parent=parent, args=args,
                         ui_filename="click_to_open.ui")

        fakeButton = self.ui.diamond
        labelWidget = self.ui.label

        clicked = QtCore.pyqtSignal(QtGui.QMouseEvent)

        def mousePressEvent(self, event):
            super().mousePressEvent(event)
            self.clicked.emit(event)
            print("i am here")

        '''
        # print(type(QtCore.QEvent.MouseButtonRelease))
        labelWidget.mousePressEvent(QMouseEvent)
        # fakeButton.mousePressEvent()
        # fakeButton.clicked.connect(the_button_was_clicked)
        print(type(fakeButton))

        def mousePressEvent(self, QMouseEvent):
            print("Mouse click detected")
            if event.button() == Qt.LeftButton:
                self.pressPos = event.pos()

        def the_button_was_clicked(self):
            print("clicked!")
        '''
