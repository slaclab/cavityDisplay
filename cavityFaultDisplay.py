from functools import partial
from typing import Dict

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout, QFrame
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

        headerLayout = QHBoxLayout()
        statusheaderLabel = QLabel()
        statusheaderLabel.setText("Status")
        statusheaderLabel.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        statusheaderLabel.setAlignment(Qt.AlignCenter)
        statusheaderLabel.setStyleSheet("text-decoration: underline")

        nameheaderLabel = QLabel()
        nameheaderLabel.setText("Name")
        nameheaderLabel.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        nameheaderLabel.setAlignment(Qt.AlignLeft)
        nameheaderLabel.setStyleSheet("text-decoration: underline")

        codeheaderLabel = QLabel()
        codeheaderLabel.setText("Code")
        codeheaderLabel.setMaximumWidth(100)
        codeheaderLabel.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        codeheaderLabel.setAlignment(Qt.AlignHCenter)
        codeheaderLabel.setStyleSheet("text-decoration: underline")

        headerLayout.addWidget(codeheaderLabel)
        headerLayout.addWidget(nameheaderLabel)
        headerLayout.addWidget(statusheaderLabel)

        headerLayout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        verticalLayout.addLayout(headerLayout)

        for fault in faults.values():
            horizontalLayout = QHBoxLayout()

            statusLabel = QLabel()
            statusLabel.setStyleSheet("font-weight: bold")
            statusLabel.setSizePolicy(QSizePolicy.MinimumExpanding,
                                      QSizePolicy.MinimumExpanding)
            statusLabel.setAlignment(Qt.AlignCenter)
            statusLabel.setFrameStyle(QFrame.Box | QFrame.Plain)
            statusLabel.setLineWidth(2)

            codeLabel = QLabel()
            codeLabel.setText(fault.tlc)
            codeLabel.setMaximumWidth(100)
            codeLabel.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
            codeLabel.setAlignment(Qt.AlignHCenter)

            shortDescriptionLabel = QLabel()
            shortDescriptionLabel.setText(fault.shortDescription)
            shortDescriptionLabel.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
            shortDescriptionLabel.setAlignment(Qt.AlignLeft)

            shortDescriptionLabel.setWordWrap(True)

            horizontalLayout.addWidget(codeLabel)
            horizontalLayout.addWidget(shortDescriptionLabel)
            horizontalLayout.addWidget(statusLabel)

            horizontalLayout.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            verticalLayout.addLayout(horizontalLayout)
            self.statusLabelCallback(statusLabel, fault)

            fault.pv.add_callback(partial(self.statusLabelCallback, statusLabel, fault))

    @staticmethod
    def statusLabelCallback(label: QLabel, fault: Fault, **kw):
        try:
            if fault.isFaulted():
                label.setText("Faulted")
                label.setStyleSheet("background-color: rgb(255,0,0);")

            else:
                label.setText("OK")
                label.setStyleSheet("background-color: rgb(0,255,0);")


        except PvInvalid:
            label.setText("Invalid")
            label.setStyleSheet("background-color: rgb(255,0,255);")
