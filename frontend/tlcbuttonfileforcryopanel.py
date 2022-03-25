from typing import List

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout
from pydm import Display

import displayCavity
from Fault import Fault


class ThreeLetterFaultDisplay(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super().__init__(parent=parent, args=args,
                         ui_filename="3letterfaults.ui",
                         macros=macros)

        cavityObject = displayCavity.DisplayCavity(self, None)

        faults: List[Fault] = cavityObject.faults
        verticalLayout: QVBoxLayout = self.ui.tlclayout

        for fault in faults.values():
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
