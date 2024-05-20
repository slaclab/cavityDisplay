from collections import OrderedDict
from dataclasses import dataclass

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout
from pydm import Display

from utils.utils import parse_csv

rows = {}


@dataclass
class Row:
    tlc: str
    longDesc: str
    genShortDesc: str


for faultRowDict in parse_csv():
    tlc = faultRowDict["Three Letter Code"]
    rows[tlc] = Row(
        tlc=tlc,
        longDesc=faultRowDict["Long Description"],
        genShortDesc=faultRowDict["Generic Short Description for Decoder"],
    )

sortedFaultRows = OrderedDict([(tlc, rows[tlc]) for tlc in sorted(rows.keys())])


class DecoderDisplay(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super().__init__(
            parent=parent, args=args, ui_filename="decoder.ui", macros=macros
        )

        verticalLayout: QVBoxLayout = self.ui.tlc_layout

        # Long description header
        headerLayout = QHBoxLayout()
        descriptionHeaderLabel = QLabel()
        descriptionHeaderLabel.setText("Description")
        descriptionHeaderLabel.setMinimumSize(200, 30)
        descriptionHeaderLabel.setStyleSheet("text-decoration: underline")

        # Name (aka short description) header
        nameHeaderLabel = QLabel()
        nameHeaderLabel.setText("Name")
        nameHeaderLabel.setMinimumSize(200, 30)
        nameHeaderLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        nameHeaderLabel.setStyleSheet("text-decoration: underline")

        # Three-Letter Code header
        codeHeaderLabel = QLabel()
        codeHeaderLabel.setText("Code")
        codeHeaderLabel.setMinimumSize(30, 30)
        codeHeaderLabel.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        codeHeaderLabel.setStyleSheet("text-decoration: underline")

        headerLayout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        headerLayout.addWidget(codeHeaderLabel)
        headerLayout.addWidget(nameHeaderLabel)
        headerLayout.addWidget(descriptionHeaderLabel)
        headerLayout.setSpacing(50)

        verticalLayout.addLayout(headerLayout)

        for row in sortedFaultRows.values():
            horizontalLayout = QHBoxLayout()
            descriptionLabel = QLabel()
            descriptionLabel.setText(row.longDesc)
            descriptionLabel.setMinimumSize(300, 50)
            descriptionLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            descriptionLabel.setWordWrap(True)

            codeLabel = QLabel()
            codeLabel.setText(row.tlc)
            codeLabel.setMinimumSize(30, 30)
            codeLabel.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

            nameLabel = QLabel()
            nameLabel.setText(row.genShortDesc)
            nameLabel.setMinimumSize(200, 50)
            nameLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
            nameLabel.setWordWrap(True)

            horizontalLayout.addWidget(codeLabel)
            horizontalLayout.addWidget(nameLabel)
            horizontalLayout.addWidget(descriptionLabel)

            horizontalLayout.setSpacing(50)
            horizontalLayout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            verticalLayout.addLayout(horizontalLayout)
