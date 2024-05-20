from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from pydm import Display
from pydm.widgets import PyDMByteIndicator, PyDMLabel, PyDMRelatedDisplayButton

from frontend.gui_cavity import GUICavity
from frontend.gui_cryomodule import GUICryomodule
from frontend.gui_linac import GUILinac
from lcls_tools.superconducting.sc_linac import Machine


class CavityDisplayGUI(Display):
    def __init__(self, parent=None, args=None):
        super().__init__(parent, args)
        self.display_machine = Machine(
            linac_class=GUILinac, cryomodule_class=GUICryomodule, cavity_class=GUICavity
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
        self.header.addWidget(self.decoder)

        self.setWindowTitle("SRF Cavity Display")

        self.vlayout = QVBoxLayout()
        self.vlayout.addLayout(self.header)
        self.setLayout(self.vlayout)

        self.top_half = QHBoxLayout()
        self.vlayout.addLayout(self.top_half)

        for i in range(0, 3):
            gui_linac: GUILinac = self.display_machine.linacs[i]
            self.top_half.addWidget(gui_linac.groupbox)

        self.vlayout.addWidget(self.display_machine.linacs[3].groupbox)
