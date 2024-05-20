from collections import OrderedDict

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout
from dataclasses import dataclass
from pydm import Display

from utils import CSV_FAULTS

rows = {}


@dataclass
class Row:
    tlc: str
    longDesc: str
    genShortDesc: str
    correctiveAction: str


for faultRowDict in CSV_FAULTS:
    tlc = faultRowDict["Three Letter Code"]
    rows[tlc] = Row(tlc=tlc, longDesc=faultRowDict["Long Description"],
                    genShortDesc=faultRowDict["Generic Short Description for Decoder"],
                    correctiveAction=faultRowDict["Recommended Corrective Actions"])

sortedFaultRows = OrderedDict([(tlc, rows[tlc]) for tlc in sorted(rows.keys())])


class DecoderDisplay(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super().__init__(parent=parent, args=args,
                         ui_filename="frontend/decoder.ui",
                         macros=macros)

        verticalLayout: QVBoxLayout = self.ui.tlc_layout
        headerLayout = QHBoxLayout()

        # Three-Letter Code header
        codeHeaderLabel = QLabel()
        codeHeaderLabel.setText("Code")
        codeHeaderLabel.setMinimumSize(30, 30)
        # codeHeaderLabel.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        codeHeaderLabel.setStyleSheet("text-decoration: underline")

        # Name (aka short description) header
        nameHeaderLabel = QLabel()
        nameHeaderLabel.setText("Name")
        nameHeaderLabel.setMinimumSize(200, 30)
        # nameHeaderLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        nameHeaderLabel.setStyleSheet("text-decoration: underline")

        # Long description header
        descriptionHeaderLabel = QLabel()
        descriptionHeaderLabel.setText("Description")
        descriptionHeaderLabel.setMinimumSize(300, 30)
        # descriptionHeaderLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        descriptionHeaderLabel.setStyleSheet("text-decoration: underline")

        # Corrective Action header
        actionHeaderLabel = QLabel()
        actionHeaderLabel.setText("Corrective Action")
        actionHeaderLabel.setMinimumSize(300, 30)
        actionHeaderLabel.setStyleSheet("text-decoration: underline")

        headerLayout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        headerLayout.addWidget(codeHeaderLabel)
        headerLayout.addWidget(nameHeaderLabel)
        headerLayout.addWidget(descriptionHeaderLabel)
        headerLayout.addWidget(actionHeaderLabel)
        headerLayout.setSpacing(50)

        verticalLayout.addLayout(headerLayout)

        for row in sortedFaultRows.values():
            horizontalLayout = QHBoxLayout()
            descriptionLabel = QLabel()
            descriptionLabel.setText(row.longDesc)
            descriptionLabel.setMinimumSize(300, 50)
            # descriptionLabel.setSizePolicy(QSizePolicy.Minimum,
            #                               QSizePolicy.Minimum)
            descriptionLabel.setWordWrap(True)

            codeLabel = QLabel()
            codeLabel.setText(row.tlc)
            codeLabel.setMinimumSize(30, 30)
            # codeLabel.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

            nameLabel = QLabel()
            nameLabel.setText(row.genShortDesc)
            nameLabel.setMinimumSize(200, 50)
            # nameLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
            nameLabel.setWordWrap(True)

            actionLabel = QLabel()
            actionLabel.setText(row.correctiveAction)
            actionLabel.setMinimumSize(300, 50)
            # actionLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
            actionLabel.setWordWrap(True)

            horizontalLayout.addWidget(codeLabel)
            horizontalLayout.addWidget(nameLabel)
            horizontalLayout.addWidget(descriptionLabel)
            horizontalLayout.addWidget(actionLabel)

            horizontalLayout.setSpacing(50)
            horizontalLayout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            verticalLayout.addLayout(horizontalLayout)
