from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout
from functools import partial
from pydm import Display
from typing import List

from DisplayCavity import DISPLAY_LINAC_OBJECTS
from Fault import Fault, PvInvalid


class CavityFaultDisplay(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super().__init__(parent=parent, args=args,
                         ui_filename="frontend/cavityfaultdisplay.ui",
                         macros=macros)

        linacIdx = int(macros["linac"][1])
        cryomoduleName = macros["cryoNum"]
        cavityNumber = macros["cavityNumber"]

        cavityObject = DISPLAY_LINAC_OBJECTS[linacIdx].cryomodules[cryomoduleName].cavities[cavityNumber]

        faults: List[Fault] = cavityObject.faults
        verticalLayout: QVBoxLayout = self.ui.cavityfaultslayout

        for fault in faults:
            horizontalLayout = QHBoxLayout()
            statusLabel = QLabel()
            statusLabel.setStyleSheet("font-weight: bold")
            statusLabel.setSizePolicy(QSizePolicy.MinimumExpanding,
                                      QSizePolicy.MinimumExpanding)

            codeLabel = QLabel()
            codeLabel.setText(fault.tlc)
            codeLabel.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

            nameLabel = QLabel()
            nameLabel.setText(fault.name)
            nameLabel.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

            horizontalLayout.addWidget(codeLabel)
            horizontalLayout.addWidget(nameLabel)
            horizontalLayout.addWidget(statusLabel)

            verticalLayout.addLayout(horizontalLayout)

            fault.pv.add_callback(partial(self.statusLabelCallback, statusLabel, fault))

    @staticmethod
    def statusLabelCallback(label: QLabel, fault: Fault, value, **kw):
        try:
            if fault.isFaulted():
                label.setText("Faulted")
            else:
                label.setText("OK")
        except PvInvalid:
            label.setText("Invalid")
