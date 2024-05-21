from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame
from pydm import Display
from pydm.widgets import PyDMByteIndicator, PyDMLabel, PyDMRelatedDisplayButton

from frontend.gui_cavity import GUICavity
from frontend.gui_cryomodule import GUICryomodule
from lcls_tools.superconducting.sc_linac import Machine


def make_line(shape=QFrame.VLine):
    line = QFrame()
    line.setFrameShape(shape)
    line.setStyleSheet("background-color: rgb(255, 255, 255);")
    return line


class CavityDisplayGUI(Display):
    def __init__(self, parent=None, args=None):
        super().__init__(parent, args)
        self.setAutoFillBackground(True)
        pal = QPalette()
        pal.setColor(QPalette.Window, QColor(40, 40, 40))
        self.setPalette(pal)

        self.setStyleSheet("color: rgb(255, 255, 255);")

        self.display_machine = Machine(
            cryomodule_class=GUICryomodule, cavity_class=GUICavity
        )

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

        self.decoder = PyDMRelatedDisplayButton(filename="frontend/decoder.py")
        self.decoder.setText("Three Letter Codes")
        self.decoder.openInNewWindow = True
        self.decoder.setStyleSheet(
            "background-color: rgb(35, 35, 35); color: rgb(255, 255, 255);"
        )
        self.header.addWidget(self.decoder)

        self.setWindowTitle("SRF Cavity Display")

        self.vlayout = QVBoxLayout()
        self.vlayout.addLayout(self.header)
        self.setLayout(self.vlayout)

        self.top_half = QHBoxLayout()
        self.bottom_half = QHBoxLayout()

        # self.top_half.addWidget(make_line())
        self.vlayout.addLayout(self.top_half)
        self.vlayout.addWidget(make_line(QFrame.HLine))

        for i in range(0, 3):
            gui_linac = self.display_machine.linacs[i]
            for gui_cm in gui_linac.cryomodules.values():
                self.top_half.addLayout(gui_cm.vlayout)

            if i != 2:
                self.top_half.addWidget(make_line())

        l3b = self.display_machine.linacs[3]
        for gui_cm in l3b.cryomodules.values():
            self.bottom_half.addLayout(gui_cm.vlayout)

        self.vlayout.addLayout(self.bottom_half)
