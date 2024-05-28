from functools import partial

from PyQt5.QtGui import QColor, QPalette, QCursor
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QPushButton,
    QApplication,
    QWidget,
)
from pydm.utilities import IconFont
from pydm.widgets import PyDMByteIndicator, PyDMLabel

from frontend.decoder import DecoderDisplay
from frontend.gui_machine import GUIMachine
from frontend.utils import make_line
from lcls_tools.common.frontend.display.util import showDisplay

app = QApplication([])


class CavityDisplayGUI(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.gui_machine = GUIMachine()
        self.setAutoFillBackground(True)
        pal = QPalette()
        pal.setColor(QPalette.Window, QColor(40, 40, 40))
        self.setPalette(pal)

        self.setStyleSheet("color: rgb(255, 255, 255);")

        self.header = QHBoxLayout()
        heartbeat_indicator = PyDMByteIndicator(
            init_channel="ALRM:SYS0:SC_CAV_FAULT:ALHBERR"
        )
        heartbeat_indicator.onColor = QColor(255, 0, 0)
        heartbeat_indicator.offColor = QColor(0, 255, 0)
        heartbeat_indicator.showLabels = False
        heartbeat_indicator.circles = True
        heartbeat_indicator.showLabels = False

        heartbeat_label = PyDMLabel(init_channel="ALRM:SYS0:SC_CAV_FAULT:ALHBERR")

        heartbeat_counter = PyDMLabel(init_channel="PHYS:SYS0:1:SC_CAV_FAULT_HEARTBEAT")

        self.header.addWidget(heartbeat_indicator)
        self.header.addWidget(heartbeat_label)
        self.header.addWidget(heartbeat_counter)
        self.header.addStretch()

        self.decoder_window: DecoderDisplay = DecoderDisplay()

        self.decoder = QPushButton("Three Letter Code Decoder")
        self.decoder.clicked.connect(partial(showDisplay, self.decoder_window))

        icon = IconFont().icon("file")
        self.decoder.setIcon(icon)
        self.decoder.setCursor(QCursor(icon.pixmap(16, 16)))
        self.decoder.openInNewWindow = True
        self.decoder.setStyleSheet(
            "background-color: rgb(35, 35, 35); color: rgb(255, 255, 255);"
        )
        self.header.addWidget(self.decoder)

        self.setWindowTitle("SRF Cavity Display")

        self.vlayout = QVBoxLayout()
        self.vlayout.addLayout(self.header)
        self.setLayout(self.vlayout)

        self.vlayout.addLayout(self.gui_machine.top_half)
        self.vlayout.addWidget(make_line(QFrame.HLine))
        self.vlayout.addLayout(self.gui_machine.bottom_half)


window = CavityDisplayGUI()
window.show()
app.exec()
