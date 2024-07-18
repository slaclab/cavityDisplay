from collections import OrderedDict

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QScrollArea,
    QGroupBox,
    QApplication,
    QAbstractScrollArea,
)
from dataclasses import dataclass
from pydm import Display

from utils.utils import parse_csv

rows = {}


@dataclass
class Row:
    tlc: str
    long_desc: str
    gen_short_desc: str
    corrective_action: str


class DecoderDisplay(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super().__init__(parent, args, macros)

        for faultRowDict in parse_csv():
            tlc = faultRowDict["Three Letter Code"]
            rows[tlc] = Row(
                tlc=tlc,
                long_desc=faultRowDict["Long Description"],
                gen_short_desc=faultRowDict["Generic Short Description for Decoder"],
                corrective_action=faultRowDict["Recommended Corrective Actions"]
            )

        sorted_fault_rows = OrderedDict(
            [(tlc, rows[tlc]) for tlc in sorted(rows.keys())]
        )

        self.setWindowTitle("Three Letter Codes")
        vlayout = QVBoxLayout()
        self.scroll_area = QScrollArea()
        vlayout.addWidget(self.scroll_area)

        self.setLayout(vlayout)

        self.groupbox = QGroupBox()
        self.scroll_area.setWidget(self.groupbox)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.scroll_area.setWidgetResizable(True)

        scroll_area_layout: QVBoxLayout = QVBoxLayout()
        self.groupbox.setLayout(scroll_area_layout)

        # Long description header
        header_layout = QHBoxLayout()
        description_header_label = QLabel("Description")
        description_header_label.setMinimumSize(100, 30)
        description_header_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        description_header_label.setStyleSheet("text-decoration: underline")

        # Name (aka short description) header
        name_header_label = QLabel("Name")
        name_header_label.setMinimumSize(100, 30)
        name_header_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        name_header_label.setStyleSheet("text-decoration: underline")

        # Three-Letter Code header
        code_header_label = QLabel("Code")
        code_header_label.setMinimumSize(30, 30)
        code_header_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        code_header_label.setStyleSheet("text-decoration: underline")

        # Corrective Action header
        action_header_label = QLabel("Corrective Action")
        action_header_label.setMinimumSize(100, 30)
        action_header_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        action_header_label.setStyleSheet("text-decoration: underline")

        header_layout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        header_layout.addWidget(code_header_label)
        header_layout.addWidget(name_header_label)
        header_layout.addWidget(description_header_label, 2)
        header_layout.addWidget(action_header_label, 2)
        header_layout.setSpacing(50)

        scroll_area_layout.addLayout(header_layout)

        for row in sorted_fault_rows.values():
            horizontal_layout = QHBoxLayout()
            description_label = QLabel(row.long_desc)
            description_label.setMinimumSize(100, 50)
            description_label.setSizePolicy(
                QSizePolicy.Minimum, QSizePolicy.Minimum
            )
            description_label.setWordWrap(True)

            code_label = QLabel(row.tlc)
            code_label.setMinimumSize(30, 30)
            code_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

            name_label = QLabel()
            name_label.setText(row.gen_short_desc)
            name_label.setMinimumSize(100, 50)
            name_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            name_label.setWordWrap(True)

            action_label = QLabel(row.corrective_action)
            action_label.setMinimumSize(100, 50)
            action_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            action_label.setWordWrap(True)

            horizontal_layout.addWidget(code_label)
            horizontal_layout.addWidget(name_label)
            horizontal_layout.addWidget(description_label, 2)
            horizontal_layout.addWidget(action_label, 2)

            horizontal_layout.setSpacing(50)
            horizontal_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            scroll_area_layout.addLayout(horizontal_layout)


def main():
    app = QApplication(sys.argv)
    decoder = DecoderDisplay()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
