import json
import sys
from typing import List

from PyQt5.QtWidgets import QHBoxLayout, QLabel
from lcls_tools.superconducting.scLinac import CRYOMODULE_OBJECTS, Cavity
from pydm import Display
from pydm.widgets import PyDMByteIndicator, PyDMEmbeddedDisplay, PyDMTemplateRepeater

from utils import DESCRIPTION_SUFFIX, SEVERITY_SUFFIX, STATUS_SUFFIX

sys.path.insert(0, "./frontend")
from cavityWidget import CavityWidget


class CavityDisplayGUI(Display):
    def __init__(self, parent=None, args=None):
        super().__init__(
            parent=parent, args=args, ui_filename="frontend/cavityDisplay.ui"
        )

        embedded_displays: List[PyDMEmbeddedDisplay] = [
            self.ui.L0B,
            self.ui.L1B,
            self.ui.L2B,
            self.ui.L3B,
        ]

        for index, linacEmbeddedDisplay in enumerate(embedded_displays):
            linacEmbeddedDisplay.loadWhenShown = False

            linac_h_layout = linacEmbeddedDisplay.findChild(QHBoxLayout)
            cryomodules_in_linac = linac_h_layout.count()

            # linac will be a list of cryomodules
            cryo_display_list: List[Display] = []
            for itemIndex in range(cryomodules_in_linac):
                cryo_display_list.append(linac_h_layout.itemAt(itemIndex).widget())

            for cryomoduleDisplay in cryo_display_list:
                cryomodule_label: QLabel = cryomoduleDisplay.children()[1]

                cm_template_repeater: PyDMTemplateRepeater = (
                    cryomoduleDisplay.children()[2]
                )

                cryomodule_object = CRYOMODULE_OBJECTS[str(cryomodule_label.text())]

                cavity_widget_list: List[
                    CavityWidget
                ] = cm_template_repeater.findChildren(CavityWidget)

                rf_status_bar_list: List[PyDMByteIndicator] = []
                ssa_status_bar_list: List[PyDMByteIndicator] = []
                status_bar_list = cm_template_repeater.findChildren(PyDMByteIndicator)

                for statusBar in status_bar_list:
                    if "RFSTATE" in statusBar.accessibleName():
                        rf_status_bar_list.append(statusBar)
                    elif "SSA" in statusBar.accessibleName():
                        ssa_status_bar_list.append(statusBar)

                for cavity_widget, rf_status_bar, ssa_status_bar in zip(
                    cavity_widget_list, rf_status_bar_list, ssa_status_bar_list
                ):
                    cavity_object: Cavity = cryomodule_object.cavities[
                        int(cavity_widget.cavityText)
                    ]

                    print(f"Creating {cavity_object} widgets")

                    severity_pv: str = cavity_object.pv_addr(SEVERITY_SUFFIX)
                    status_pv: str = cavity_object.pv_addr(STATUS_SUFFIX)
                    description_pv: str = cavity_object.pv_addr(DESCRIPTION_SUFFIX)
                    rf_state_pv: str = cavity_object.rf_state_pv_obj.pvname
                    ssa_pv: str = cavity_object.ssa.status_pv

                    rf_status_bar.channel = rf_state_pv
                    ssa_status_bar.channel = ssa_pv

                    cavity_widget.channel = status_pv
                    cavity_widget.severity_channel = severity_pv
                    cavity_widget.description_channel = description_pv
                    cavity_widget.cavityNumber = cavity_object.number
                    cavity_widget.cmName = cavity_object.cryomodule.name

                    rule = [
                        {
                            "channels": [
                                {"channel": ssa_pv, "trigger": True, "use_enum": True}
                            ],
                            "property": "Opacity",
                            "expression": "ch[0] == 'SSA On'",
                            "initial_value": "0",
                            "name": "show",
                        }
                    ]

                    ssa_status_bar.rules = json.dumps(rule)
