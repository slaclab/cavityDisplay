import sys
from collections import OrderedDict
from dataclasses import dataclass

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
from pydm import Display

from utils.utils import parse_csv

rows = {}


@dataclass
class Row:
    tlc: str
    longDesc: str
    genShortDesc: str


class DecoderDisplay(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super().__init__(parent, args, macros)

        for faultRowDict in parse_csv():
            tlc = faultRowDict["Three Letter Code"]
            rows[tlc] = Row(
                tlc=tlc,
                longDesc=faultRowDict["Long Description"],
                genShortDesc=faultRowDict["Generic Short Description for Decoder"],
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
        description_header_label.setMinimumSize(200, 30)
        description_header_label.setStyleSheet("text-decoration: underline")

        # Name (aka short description) header
        name_header_label = QLabel("Name")
        name_header_label.setMinimumSize(200, 30)
        name_header_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        name_header_label.setStyleSheet("text-decoration: underline")

        # Three-Letter Code header
        code_header_label = QLabel("Code")
        code_header_label.setMinimumSize(30, 30)
        code_header_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        code_header_label.setStyleSheet("text-decoration: underline")

        header_layout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        header_layout.addWidget(code_header_label)
        header_layout.addWidget(name_header_label)
        header_layout.addWidget(description_header_label)
        header_layout.setSpacing(50)

        scroll_area_layout.addLayout(header_layout)

        for row in sorted_fault_rows.values():
            horizontal_layout = QHBoxLayout()
            description_label = QLabel(row.longDesc)
            description_label.setMinimumSize(300, 50)
            description_label.setSizePolicy(
                QSizePolicy.MinimumExpanding, QSizePolicy.Minimum
            )
            description_label.setWordWrap(True)

            code_label = QLabel(row.tlc)
            code_label.setMinimumSize(30, 30)
            code_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

            name_label = QLabel()
            name_label.setText(row.genShortDesc)
            name_label.setMinimumSize(200, 50)
            name_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
            name_label.setWordWrap(True)

            horizontal_layout.addWidget(code_label)
            horizontal_layout.addWidget(name_label)
            horizontal_layout.addWidget(description_label)

            horizontal_layout.setSpacing(50)
            horizontal_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            scroll_area_layout.addLayout(horizontal_layout)


def main():
    app = QApplication(sys.argv)
    decoder = DecoderDisplay()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
