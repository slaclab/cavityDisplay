import json
from typing import TYPE_CHECKING

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QSizePolicy
from frontend.cavity_widget import CavityWidget
from pydm.widgets import PyDMByteIndicator

from lcls_tools.superconducting.sc_linac import Cavity

if TYPE_CHECKING:
    from lcls_tools.superconducting.sc_linac import Rack


class GUICavity(Cavity):
    def __init__(self, cavity_num: int, rack_object: "Rack"):
        super().__init__(cavity_num, rack_object)
        self.vert_layout = QVBoxLayout()
        self.cavity_widget = CavityWidget()
        self.cavity_widget.setMinimumSize(10, 10)
        self.cavity_widget.setAccessibleName("cavity_widget")
        self.cavity_widget.cavityText = str(cavity_num)
        self.cavity_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.hor_layout = QHBoxLayout()

        self.ssa_bar = PyDMByteIndicator()
        self.ssa_bar.setAccessibleName("SSA")
        self.ssa_bar.onColor = QColor(92, 255, 92)
        self.ssa_bar.offColor = QColor(40, 40, 40)
        self.ssa_bar.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        self.ssa_bar.showLabels = False
        self.ssa_bar.channel = self.ssa.status_pv
        self.ssa_bar.setFixedHeight(5)

        self.rf_bar = PyDMByteIndicator()
        self.rf_bar.setAccessibleName("RFSTATE")
        self.rf_bar.onColor = QColor(14, 191, 255)
        self.rf_bar.offColor = QColor(40, 40, 40)
        self.rf_bar.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        self.rf_bar.showLabels = False
        self.rf_bar.channel = self.rf_state_pv
        self.rf_bar.setFixedHeight(5)

        self.hor_layout.addWidget(self.ssa_bar)
        self.hor_layout.addWidget(self.rf_bar)

        self.vert_layout.addWidget(self.cavity_widget)
        self.vert_layout.addLayout(self.hor_layout)

        severity_pv: str = self.pv_addr("CUDSEVR")
        status_pv: str = self.pv_addr("CUDSTATUS")
        description_pv: str = self.pv_addr("CUDDESC")

        self.cavity_widget.channel = status_pv
        self.cavity_widget.severity_channel = severity_pv
        self.cavity_widget.description_channel = description_pv

        rule = [
            {
                "channels": [
                    {"channel": self.ssa.status_pv, "trigger": True, "use_enum": True}
                ],
                "property": "Opacity",
                "expression": "ch[0] == 'SSA On'",
                "initial_value": "0",
                "name": "show",
            }
        ]

        self.ssa_bar.rules = json.dumps(rule)
