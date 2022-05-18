from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout
from functools import partial
from pydm import Display
from typing import Dict

from Fault import Fault, PvInvalid
from displayCavity import DISPLAY_CRYOMODULES


class CavityFaultDisplay(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super().__init__(parent=parent, args=args,
                         ui_filename="frontend/cavityfaultdisplay.ui",
                         macros=macros)

        cryomoduleName = macros["cryoNum"]
        cavityNumber = macros["cavityNumber"]

        cavityObject = DISPLAY_CRYOMODULES[cryomoduleName].cavities[cavityNumber]

        faults: Dict[str, Fault] = cavityObject.faults
        verticalLayout: QVBoxLayout = self.ui.cavityfaultslayout

        headerLayout = QHBoxLayout()
        statusheaderLabel = QLabel()
        statusheaderLabel.setText("Status")
        statusheaderLabel.setMaximumWidth(100)
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
        codeheaderLabel.setMaximumWidth(50)
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
            statusLabel.setMaximumWidth(100)
            statusLabel.setMaximumHeight(28)
            statusLabel.setMinimumHeight(28)
            statusLabel.setSizePolicy(QSizePolicy.MinimumExpanding,
                                      QSizePolicy.MinimumExpanding)
            statusLabel.setAlignment(Qt.AlignCenter)

            codeLabel = QLabel()
            codeLabel.setText(fault.tlc)
            codeLabel.setMaximumWidth(50)
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
            self.statusLabelCallback(statusLabel, codeLabel, fault)

            fault.pv.add_callback(partial(self.statusLabelCallback, statusLabel, codeLabel, fault))

    @staticmethod
    def statusLabelCallback(statuslabel: QLabel, codelabel: QLabel, fault: Fault, **kw):
        try:
            if fault.isFaulted():
                statuslabel.setText("FAULTED")
                statuslabel.setStyleSheet("background-color: rgb(255,0,0); font-weight: "
                                          "bold; border: 2px solid black; color: white;")
                codelabel.setStyleSheet("font-weight:bold;")

            else:
                statuslabel.setText("OK")
                statuslabel.setStyleSheet("background-color: rgb(0,255,0);font-weight: bold; "
                                          "border: 2px solid black;")
                codelabel.setStyleSheet("font-weight:plain;")



        except PvInvalid:
            statuslabel.setText("INVALID")
            statuslabel.setStyleSheet("background-color: rgb(255,0,255);font-weight: bold;"
                                      "border: 2px solid black;")
