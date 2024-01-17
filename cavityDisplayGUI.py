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

        embeddedDisplays: List[PyDMEmbeddedDisplay] = [
            self.ui.L0B,
            self.ui.L1B,
            self.ui.L2B,
            self.ui.L3B,
        ]

        for index, linacEmbeddedDisplay in enumerate(embeddedDisplays):
            linacEmbeddedDisplay.loadWhenShown = False

            linacHorizLayout = linacEmbeddedDisplay.findChild(QHBoxLayout)
            totalCryosInLinac = linacHorizLayout.count()

            # linac will be a list of cryomodules
            cryoDisplayList: List[Display] = []
            for itemIndex in range(totalCryosInLinac):
                cryoDisplayList.append(linacHorizLayout.itemAt(itemIndex).widget())

            for cryomoduleDisplay in cryoDisplayList:
                cryomoduleLabel: QLabel = cryomoduleDisplay.children()[1]

                cmTemplateRepeater: PyDMTemplateRepeater = cryomoduleDisplay.children()[
                    2
                ]

                cryomoduleObject = CRYOMODULE_OBJECTS[str(cryomoduleLabel.text())]

                cavityWidgetList: List[CavityWidget] = cmTemplateRepeater.findChildren(
                    CavityWidget
                )

                rfStatusBarList: List[PyDMByteIndicator] = []
                ssaStatusBarList: List[PyDMByteIndicator] = []
                statusBarList = cmTemplateRepeater.findChildren(PyDMByteIndicator)
                for statusBar in statusBarList:
                    if "RFSTATE" in statusBar.accessibleName():
                        rfStatusBarList.append(statusBar)
                    elif "SSA" in statusBar.accessibleName():
                        ssaStatusBarList.append(statusBar)

                for cavityWidget, rfStatusBar, ssaStatusBar in zip(
                    cavityWidgetList, rfStatusBarList, ssaStatusBarList
                ):
                    cavityObject: Cavity = cryomoduleObject.cavities[
                        int(cavityWidget.cavityText)
                    ]

                    print(f"Creating {cavityObject} widgets")

                    severityPV: str = cavityObject.pv_addr(SEVERITY_SUFFIX)
                    statusPV: str = cavityObject.pv_addr(STATUS_SUFFIX)
                    descriptionPV: str = cavityObject.pv_addr(DESCRIPTION_SUFFIX)
                    rfStatePV: str = cavityObject.rf_state_pv_obj.pvname
                    ssaPV: str = cavityObject.ssa.status_pv

                    rfStatusBar.channel = rfStatePV
                    ssaStatusBar.channel = ssaPV

                    cavityWidget.channel = statusPV
                    cavityWidget.severity_channel = severityPV
                    cavityWidget.description_channel = descriptionPV
                    cavityWidget.cavityNumber = cavityObject.number
                    cavityWidget.cmName = cavityObject.cryomodule.name

                    rule = [
                        {
                            "channels": [
                                {"channel": ssaPV, "trigger": True, "use_enum": True}
                            ],
                            "property": "Opacity",
                            "expression": "ch[0] == 'SSA On'",
                            "initial_value": "0",
                            "name": "show",
                        }
                    ]

                    ssaStatusBar.rules = json.dumps(rule)
