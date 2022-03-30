from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout
from functools import partial
from pydm import Display
from typing import Dict

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout
from pydm import Display
from typing import Dict

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
        statusheaderLabel.setStyleSheet("text-decoration: underline")

        nameheaderLabel = QLabel()
        nameheaderLabel.setText("Name")
        nameheaderLabel.setMinimumSize(200, 30)
        nameheaderLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        nameheaderLabel.setStyleSheet("text-decoration: underline")

        codeheaderLabel = QLabel()
        codeheaderLabel.setText("Code")
        codeheaderLabel.setMinimumSize(30, 30)
        codeheaderLabel.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        codeheaderLabel.setStyleSheet("text-decoration: underline")

        headerLayout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        headerLayout.addWidget(codeheaderLabel)
        headerLayout.addWidget(nameheaderLabel)
        headerLayout.addWidget(statusheaderLabel)
        headerLayout.setSpacing(50)

        verticalLayout.addLayout(headerLayout)

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

            shortDescriptionLabel = QLabel()
            shortDescriptionLabel.setText(fault.shortDescription)
            shortDescriptionLabel.setMinimumSize(200, 30)
            shortDescriptionLabel.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
            shortDescriptionLabel.setWordWrap(True)

            horizontalLayout.addWidget(codeLabel)
            horizontalLayout.addWidget(shortDescriptionLabel)
            horizontalLayout.addWidget(statusLabel)

            horizontalLayout.setSpacing(50)
            horizontalLayout.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
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
