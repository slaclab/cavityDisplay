from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel

from lcls_tools.superconducting.sc_linac import Cryomodule


class GUICryomodule(Cryomodule):
    def __init__(self, cryo_name: str, linac_object: "Linac"):
        super().__init__(cryo_name, linac_object)
        self.vlayout = QVBoxLayout()
        self.label = QLabel(cryo_name)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet(
            "background-color: rgb(35, 35, 35); color: rgb(255, 255, 255);"
        )
        self.vlayout.addWidget(self.label)
        for gui_cavity in self.cavities.values():
            self.vlayout.addLayout(gui_cavity.vert_layout)
