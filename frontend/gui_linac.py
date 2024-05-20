from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QSizePolicy

from lcls_tools.superconducting.sc_linac import Linac


class GUILinac(Linac):
    def __init__(
        self,
        linac_section,
        beamline_vacuum_infixes,
        insulating_vacuum_cryomodules,
        machine,
    ):
        super().__init__(
            linac_section,
            beamline_vacuum_infixes,
            insulating_vacuum_cryomodules,
            machine,
        )

        self.groupbox = QGroupBox()
        self.groupbox.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.groupbox.setStyleSheet(
            "color: rgb(255, 255, 255); background-color: rgb(40, 40, 40);"
        )
        self.groupbox.setTitle(f"L{linac_section}B")
        font = QFont()
        font.setPointSize(15)
        font.setWeight(75)
        font.setBold(True)
        self.groupbox.setFont(font)
        self.groupbox.setAlignment(Qt.AlignCenter)

        self.cm_layout = QHBoxLayout()
        for gui_cm in self.cryomodules.values():
            self.cm_layout.addLayout(gui_cm.vlayout)

        self.groupbox.setLayout(self.cm_layout)
