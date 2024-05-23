from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QGridLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QScrollArea,
    QAbstractScrollArea,
    QGroupBox,
)
from edmbutton import PyDMEDMDisplayButton
from pydm import Display
from pydm.widgets import PyDMLabel, PyDMRelatedDisplayButton, PyDMShellCommand

from backend.backend_cavity import BackendCavity
from backend.backend_cryomodule import BackendCryomodule
from backend.backend_ssa import BackendSSA
from backend.fault import PVInvalidError
from lcls_tools.superconducting.sc_linac import Machine

BACKEND_MACHINE = Machine(
    cavity_class=BackendCavity, cryomodule_class=BackendCryomodule, ssa_class=BackendSSA
)


class PyDMFaultButton(PyDMRelatedDisplayButton):
    def __init__(self):
        super().__init__()

    def push_button_release_event(self, mouse_event) -> None:
        for item in self._get_items():
            self.open_display(
                item["filename"],
                item["macros"],
                target=PyDMRelatedDisplayButton.NEW_WINDOW,
            )


class FaultCavity(BackendCavity):
    def __init__(self, cavity_num, rack_object):
        super().__init__(cavity_num, rack_object)

        self.grid_layout = None
        self._display: Optional[Display] = None

    def populate_faults(self):
        for idx, fault in enumerate(self.faults.values()):
            code_label = QLabel(fault.tlc)
            code_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
            code_label.setAlignment(Qt.AlignCenter)

            short_description_label = QLabel(fault.short_description)
            short_description_label.setSizePolicy(
                QSizePolicy.Maximum, QSizePolicy.Maximum
            )
            short_description_label.setAlignment(Qt.AlignLeft)
            short_description_label.setWordWrap(True)

            action_label = QLabel(fault.action)
            action_label.setSizePolicy(
                QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
            )
            action_label.setAlignment(Qt.AlignLeft)
            action_label.setWordWrap(True)

            status_label = EnumLabel(fault=fault, codeLabel=code_label)
            status_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

            row_idx = idx + 1
            self.grid_layout.addWidget(code_label, row_idx, 0)
            self.grid_layout.addWidget(short_description_label, row_idx, 1)
            self.grid_layout.addWidget(status_label, row_idx, 2)

            if fault.button_level == "EDM":
                button = PyDMEDMDisplayButton()
                button.filenames = [fault.button_command]
                button.macros = fault.macros + (
                    "," + fault.button_macro if fault.button_macro else ""
                )

            elif fault.button_level == "SCRIPT":
                button = PyDMShellCommand()
                button.commands = [fault.button_command]
                print(button.commands)

            elif fault.button_level == "PYDM":
                button = PyDMFaultButton()
                button.openInNewWindow = True
                button.filenames = [fault.button_command]
                button.macros = self.cryomodule.pydm_macros

            else:
                button = PyDMRelatedDisplayButton()
                button.setEnabled(False)

            self.grid_layout.addWidget(button, row_idx, 3)
            self.grid_layout.addWidget(action_label, row_idx, 4)
            button.setText(fault.button_text)
            button.showIcon = False

    @property
    def display(self):
        if not self._display:
            groupbox = QGroupBox()
            self.grid_layout = self.make_header()
            groupbox.setLayout(self.grid_layout)
            self.populate_faults()

            self._display = Display()
            self._display.setWindowTitle(f"{self} Faults")
            vlayout = QVBoxLayout()

            self._display.setLayout(vlayout)

            scroll_area = QScrollArea()
            scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            scroll_area.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
            scroll_area.setWidgetResizable(True)
            vlayout.addWidget(scroll_area)
            scroll_area.setWidget(groupbox)

        return self._display

    def make_header(self) -> QGridLayout:
        grid_layout: QGridLayout = QGridLayout()
        status_header_label = QLabel("Status")
        status_header_label.setAlignment(Qt.AlignHCenter)
        status_header_label.setStyleSheet("text-decoration:underline")

        name_header_label = QLabel("Name")
        name_header_label.setAlignment(Qt.AlignLeft)
        name_header_label.setStyleSheet("text-decoration:underline")

        code_header_label = QLabel("Code")
        code_header_label.setAlignment(Qt.AlignHCenter)
        code_header_label.setStyleSheet("text-decoration:underline")

        button_header_label = QLabel("Panel")
        button_header_label.setAlignment(Qt.AlignHCenter)
        button_header_label.setStyleSheet("text-decoration:underline")

        action_header_label: QLabel = QLabel("Recommended Corrective Action")
        action_header_label.setAlignment(Qt.AlignHCenter)
        action_header_label.setStyleSheet("text-decoration:underline")

        grid_layout.addWidget(code_header_label, 0, 0)
        grid_layout.addWidget(name_header_label, 0, 1)
        grid_layout.addWidget(status_header_label, 0, 2)
        grid_layout.addWidget(button_header_label, 0, 3)
        grid_layout.addWidget(action_header_label, 0, 4)
        return grid_layout


class EnumLabel(PyDMLabel):
    """
    PyDMLabel subclass to change PyDMLabel Alarm channel text
    """

    def __init__(self, fault, codeLabel, parent=None, args=None):
        super(EnumLabel, self).__init__(parent=parent, init_channel=fault.pv.pvname)
        self.fault = fault
        self.codeLabel = codeLabel

        self.setMaximumWidth(100)
        self.setMaximumHeight(28)
        self.setMinimumHeight(28)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.setAlignment(Qt.AlignCenter)

    def value_changed(self, new_value):
        super(EnumLabel, self).value_changed(new_value)
        try:
            if self.fault.is_currently_faulted():
                self.setText("FAULTED")
                self.setStyleSheet(
                    "background-color: rgb(255,0,0); font-weight: "
                    "bold; border: 2px solid black; color: white;"
                )
                self.codeLabel.setStyleSheet("font-weight:bold;")

            else:
                self.setText("OK")
                self.setStyleSheet(
                    "background-color: rgb(0,255,0);font-weight: bold; "
                    "border: 2px solid black;"
                )
                self.codeLabel.setStyleSheet("font-weight:plain;")

        except PVInvalidError:
            self.setText("INVALID")
            self.setStyleSheet(
                "background-color: rgb(255,0,255);font-weight: bold;"
                "border: 2px solid black;"
            )
            self.codeLabel.setStyleSheet("font-weight:bold;")
