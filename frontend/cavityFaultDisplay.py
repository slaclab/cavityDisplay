import sys
from typing import Dict

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout
from edmbutton import PyDMEDMDisplayButton
from pydm import Display
from pydm.widgets import PyDMLabel, PyDMRelatedDisplayButton, PyDMShellCommand

sys.path.insert(0, '..')
from displayLinac import DISPLAY_CRYOMODULES
from fault import Fault, PvInvalid


class PyDMFaultButton(PyDMRelatedDisplayButton):
    def __init__(self):
        super().__init__()
    
    def push_button_release_event(self, mouse_event) -> None:
        for item in self._get_items():
            self.open_display(item['filename'], item['macros'],
                              target=PyDMRelatedDisplayButton.NEW_WINDOW)


class CavityFaultDisplay(Display):
    def __init__(self, cavityNumber, cmName, parent=None, args=None):
        super().__init__(parent=parent, args=args,
                         ui_filename="cavityfaultdisplay.ui")
        
        cryomoduleName = cmName
        cavityNumber = cavityNumber
        self.ui.label.setText(f"CM{cryomoduleName} Cavity {cavityNumber} Faults")
        
        cavityObject = DISPLAY_CRYOMODULES[cryomoduleName].cavities[cavityNumber]
        
        faults: Dict[str, Fault] = cavityObject.faults
        verticalLayout: QVBoxLayout = self.ui.cavityfaultslayout
        
        headerLayout = QHBoxLayout()
        statusheaderLabel = QLabel()
        statusheaderLabel.setText("Status")
        statusheaderLabel.setMaximumWidth(100)
        statusheaderLabel.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        statusheaderLabel.setAlignment(Qt.AlignHCenter)
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
        
        buttonheaderLabel = QLabel()
        buttonheaderLabel.setText("Panel")
        buttonheaderLabel.setMaximumWidth(58)
        buttonheaderLabel.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        buttonheaderLabel.setAlignment(Qt.AlignHCenter)
        buttonheaderLabel.setStyleSheet("text-decoration:underline")
        
        headerLayout.addWidget(codeheaderLabel)
        headerLayout.addWidget(nameheaderLabel)
        headerLayout.addWidget(statusheaderLabel)
        headerLayout.addWidget(buttonheaderLabel)
        
        headerLayout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        verticalLayout.addLayout(headerLayout)
        
        for fault in faults.values():
            horizontalLayout = QHBoxLayout()
            
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
            
            statusLabel = EnumLabel(fault=fault, codeLabel=codeLabel)
            statusLabel.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
            
            horizontalLayout.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            
            horizontalLayout.addWidget(codeLabel)
            horizontalLayout.addWidget(shortDescriptionLabel)
            horizontalLayout.addWidget(statusLabel)
            
            if fault.button_level == "EDM":
                button = PyDMEDMDisplayButton()
                button.filenames = [fault.button_command]
                button.macros = fault.macros + (',' + fault.button_macro if fault.button_macro else "")
            
            elif fault.button_level == "SCRIPT":
                button = PyDMShellCommand()
                button.commands = [fault.button_command]
                print(button.commands)
            
            elif fault.button_level == "PYDM":
                button = PyDMFaultButton()
                button.openInNewWindow = True
                button.filenames = [fault.button_command]
                button.macros = cavityObject.cryomodule.pydm_macros
            
            else:
                button = PyDMRelatedDisplayButton()
                button.setEnabled(False)
            
            horizontalLayout.addWidget(button)
            button.setText(fault.button_text)
            button.showIcon = False
            verticalLayout.addLayout(horizontalLayout)


class EnumLabel(PyDMLabel):
    """
    PyDMLabel subclass to change PyDMLabel Alarm channel text
    """
    
    def __init__(self, fault, codeLabel, parent=None, args=None):
        super(EnumLabel, self).__init__(parent=parent,
                                        init_channel=fault.pv.pvname)
        self.fault = fault
        self.codeLabel = codeLabel
        
        self.setMaximumWidth(100)
        self.setMaximumHeight(28)
        self.setMinimumHeight(28)
        self.setSizePolicy(QSizePolicy.MinimumExpanding,
                           QSizePolicy.MinimumExpanding)
        self.setAlignment(Qt.AlignCenter)
    
    def value_changed(self, new_value):
        super(EnumLabel, self).value_changed(new_value)
        try:
            if self.fault.isFaulted():
                self.setText("FAULTED")
                self.setStyleSheet("background-color: rgb(255,0,0); font-weight: "
                                   "bold; border: 2px solid black; color: white;")
                self.codeLabel.setStyleSheet("font-weight:bold;")
            
            else:
                self.setText("OK")
                self.setStyleSheet("background-color: rgb(0,255,0);font-weight: bold; "
                                   "border: 2px solid black;")
                self.codeLabel.setStyleSheet("font-weight:plain;")
        
        except PvInvalid:
            self.setText("INVALID")
            self.setStyleSheet("background-color: rgb(255,0,255);font-weight: bold;"
                               "border: 2px solid black;")
            self.codeLabel.setStyleSheet("font-weight:bold;")
