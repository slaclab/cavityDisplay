import sys
from typing import Dict

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QLabel, QSizePolicy
from edmbutton import PyDMEDMDisplayButton
from pydm import Display
from pydm.widgets import PyDMLabel, PyDMRelatedDisplayButton, PyDMShellCommand

sys.path.insert(0, "..")
from display_linac import DISPLAY_MACHINE
from fault import Fault, PVInvalidError


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


class CavityFaultDisplay(Display):
    def __init__(self, cavity_number, cmName, parent=None, args=None):
        super().__init__(
            parent=parent, args=args, ui_filename="cavity_fault_display.ui"
        )

        cryomodule_name = cmName
        cavity_number = cavity_number
        self.ui.label.setText(f"CM{cryomodule_name} Cavity {cavity_number} Faults")

        cavity_object = DISPLAY_MACHINE.cryomodules[cryomodule_name].cavities[
            cavity_number
        ]

        faults: Dict[str, Fault] = cavity_object.faults

        grid_layout: QGridLayout = self.ui.cavityfaultslayout

        status_header_label = QLabel()
        status_header_label.setText("Status")
        status_header_label.setAlignment(Qt.AlignHCenter)
        status_header_label.setStyleSheet("text-decoration: underline")

        name_header_label = QLabel()
        name_header_label.setText("Name")
        name_header_label.setAlignment(Qt.AlignLeft)
        name_header_label.setStyleSheet("text-decoration: underline")

        code_header_label = QLabel()
        code_header_label.setText("Code")
        code_header_label.setAlignment(Qt.AlignHCenter)
        code_header_label.setStyleSheet("text-decoration: underline")

        button_header_label = QLabel()
        button_header_label.setText("Panel")
        button_header_label.setAlignment(Qt.AlignHCenter)
        button_header_label.setStyleSheet("text-decoration:underline")

        action_header_label: QLabel = QLabel()
        action_header_label.setText("Recommended Corrective Action")
        action_header_label.setAlignment(Qt.AlignHCenter)
        action_header_label.setStyleSheet("text-decoration:underline")

        grid_layout.addWidget(code_header_label, 0, 0)
        grid_layout.addWidget(name_header_label, 0, 1)
        grid_layout.addWidget(status_header_label, 0, 2)
        grid_layout.addWidget(button_header_label, 0, 3)
        grid_layout.addWidget(action_header_label, 0, 4)

        for idx, fault in enumerate(faults.values()):
            # horizontalLayout = QHBoxLayout()

            code_label = QLabel()
            code_label.setText(fault.tlc)
            # code_label.setMaximumWidth(50)
            code_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
            code_label.setAlignment(Qt.AlignCenter)

            short_description_label = QLabel()
            short_description_label.setText(fault.short_description)
            short_description_label.setSizePolicy(
                QSizePolicy.Maximum, QSizePolicy.Maximum
            )
            short_description_label.setAlignment(Qt.AlignLeft)
            short_description_label.setWordWrap(True)

            action_label = QLabel()
            action_label.setText(fault.action)
            action_label.setSizePolicy(
                QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
            )
            action_label.setAlignment(Qt.AlignLeft)
            action_label.setWordWrap(True)

            status_label = EnumLabel(fault=fault, codeLabel=code_label)
            status_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

            row_idx = idx + 1
            grid_layout.addWidget(code_label, row_idx, 0)
            grid_layout.addWidget(short_description_label, row_idx, 1)
            grid_layout.addWidget(status_label, row_idx, 2)

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
                button.macros = cavity_object.cryomodule.pydm_macros

            else:
                button = PyDMRelatedDisplayButton()
                button.setEnabled(False)

            grid_layout.addWidget(button, row_idx, 3)
            grid_layout.addWidget(action_label, row_idx, 4)
            button.setText(fault.button_text)
            button.showIcon = False


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
