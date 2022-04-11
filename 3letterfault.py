from dataclasses import dataclass

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout
from pydm import Display

from constants import CSV_FAULTS

rows = {}


@dataclass
class Row:
    tlc: str
    longDesc: str
    shortDesc: str


for faultRowDict in CSV_FAULTS:
    tlc = faultRowDict["Three Letter Code"]
    rows[tlc] = Row(tlc=tlc, longDesc=faultRowDict["Long Description"],
                    shortDesc=faultRowDict["Short Description"])


class ThreeLetterFaultDisplay(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super().__init__(parent=parent, args=args,
                         ui_filename="frontend/3letterfaults.ui",
                         macros=macros)

        verticalLayout: QVBoxLayout = self.ui.tlclayout

        headerLayout = QHBoxLayout()
        descriptionheaderLabel = QLabel()
        descriptionheaderLabel.setText("Description")
        descriptionheaderLabel.setMinimumSize(200, 30)
        descriptionheaderLabel.setStyleSheet("text-decoration: underline")

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
        headerLayout.addWidget(descriptionheaderLabel)
        headerLayout.setSpacing(50)

        verticalLayout.addLayout(headerLayout)

        for row in rows.values():
            horizontalLayout = QHBoxLayout()
            descriptionLabel = QLabel()
            descriptionLabel.setText(row.longDesc)
            descriptionLabel.setMinimumSize(300, 50)
            descriptionLabel.setSizePolicy(QSizePolicy.Minimum,
                                           QSizePolicy.Minimum)
            descriptionLabel.setWordWrap(True)

            codeLabel = QLabel()
            codeLabel.setText(row.tlc)
            codeLabel.setMinimumSize(30, 30)
            codeLabel.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

            nameLabel = QLabel()
            nameLabel.setText(row.shortDesc)
            nameLabel.setMinimumSize(200, 50)
            nameLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
            nameLabel.setWordWrap(True)

            horizontalLayout.addWidget(codeLabel)
            horizontalLayout.addWidget(nameLabel)
            horizontalLayout.addWidget(descriptionLabel)

            horizontalLayout.setSpacing(50)
            horizontalLayout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            verticalLayout.addLayout(horizontalLayout)
