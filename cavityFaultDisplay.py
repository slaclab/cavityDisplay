from functools import partial
from typing import Dict

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout
from pydm import Display

from Fault import Fault, PvInvalid
from displayCavity import DISPLAY_LINAC_OBJECTS


class CavityFaultDisplay(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super().__init__(parent=parent, args=args,
                         ui_filename="frontend/cavityfaultdisplay.ui",
                         macros=macros)

        linacIdx = int(macros["linac"][1])
        cryomoduleName = macros["cryoNum"]
        cavityNumber = macros["cavityNumber"]

        cavityObject = DISPLAY_LINAC_OBJECTS[linacIdx].cryomodules[cryomoduleName].cavities[cavityNumber]

        faults: Dict[str, Fault] = cavityObject.faults
        verticalLayout: QVBoxLayout = self.ui.cavityfaultslayout

        for fault in faults.values():
            horizontalLayout = QHBoxLayout()

            statusLabel = QLabel()
            statusLabel.setStyleSheet("font-weight: bold")
            statusLabel.setSizePolicy(QSizePolicy.MinimumExpanding,
                                      QSizePolicy.MinimumExpanding)

            codeLabel = QLabel()
            codeLabel.setText(fault.tlc)
            codeLabel.setMinimumSize(30, 30)
            codeLabel.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

            nameLabel = QLabel()
            nameLabel.setText(fault.name)
            nameLabel.setMinimumSize(200, 30)
            nameLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
            nameLabel.setWordWrap(True)

            horizontalLayout.addWidget(codeLabel)
            horizontalLayout.addWidget(nameLabel)
            horizontalLayout.addWidget(statusLabel)

            horizontalLayout.setAlignment(Qt.AlignLeft | Qt.AlignHCenter)
            horizontalLayout.setSpacing(50)

            verticalLayout.addLayout(horizontalLayout)
            self.statusLabelCallback(statusLabel, fault)

            fault.pv.add_callback(partial(self.statusLabelCallback, statusLabel, fault))
        verticalLayout.setSpacing(10)

    @staticmethod
    def statusLabelCallback(label: QLabel, fault: Fault, **kw):
        try:
            if fault.isFaulted():
                label.setText("Faulted")
            else:
                label.setText("OK")
        except PvInvalid:
            label.setText("Invalid")
