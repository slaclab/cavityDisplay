from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout
from functools import partial
from pydm import Display
from typing import List

from displayCavity import DISPLAY_LINAC_OBJECTS
from Fault import Fault, PvInvalid

class ThreeLetterFaultDisplay(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super().__init__(parent=parent, args=args,
                         ui_filename="frontend/3letterfaults.ui",
                         macros=macros)

        linacIdx = int(macros["linac"][1])
        cryomoduleName = macros["cryoNum"]
        cavityNumber = macros["cavityNumber"]

        cavityObject = DISPLAY_LINAC_OBJECTS[linacIdx].cryomodules[cryomoduleName].cavities[cavityNumber]

        faults: List[Fault] = cavityObject.faults
        verticalLayout: QVBoxLayout = self.ui.tlclayout

        for fault in faults:
            horizontalLayout = QHBoxLayout()
            descriptionLabel = QLabel()
            descriptionLabel.setText(fault.description)
            descriptionLabel.setSizePolicy(QSizePolicy.MinimumExpanding,
                                           QSizePolicy.MinimumExpanding)

            codeLabel = QLabel()
            codeLabel.setText(fault.tlc)
            codeLabel.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

            nameLabel = QLabel()
            nameLabel.setText(fault.name)
            nameLabel.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

            horizontalLayout.addWidget(codeLabel)
            horizontalLayout.addWidget(nameLabel)
            horizontalLayout.addWidget(descriptionLabel)

            verticalLayout.addLayout(horizontalLayout)