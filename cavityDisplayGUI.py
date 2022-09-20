import json
import sys
from PyQt5.QtWidgets import QHBoxLayout
from pydm import Display
from pydm.widgets import (PyDMByteIndicator, PyDMEmbeddedDisplay, PyDMRelatedDisplayButton,
                          PyDMTemplateRepeater)
from typing import List

from lcls_tools.superconducting.scLinac import CRYOMODULE_OBJECTS, Cavity

sys.path.insert(0, './frontend')
from cavityWidget import CavityWidget

STATUS_SUFFIX = "CUDSTATUS"
SEVERITY_SUFFIX = "CUDSEVR"
DESCRIPTION_SUFFIX = "CUDDESC"
RF_STATUS_SUFFIX = "RFSTATE"


class CavityDisplayGUI(Display):

    def __init__(self, parent=None, args=None):
        super().__init__(parent=parent, args=args,
                         ui_filename="frontend/cavityDisplay.ui")

        embeddedDisplays: List[PyDMEmbeddedDisplay] = [self.ui.L0B,
                                                       self.ui.L1B,
                                                       self.ui.L2B,
                                                       self.ui.L3B]

        for index, linacEmbeddedDisplay in enumerate(embeddedDisplays):
            linacEmbeddedDisplay.loadWhenShown = False
            print("loading L{linac}B embedded display".format(linac=index))

            linacHorizLayout = linacEmbeddedDisplay.findChild(QHBoxLayout)
            totalCryosInLinac = linacHorizLayout.count()

            # linac will be a list of cryomodules
            cryoDisplayList: List[Display] = []
            for itemIndex in range(totalCryosInLinac):
                cryoDisplayList.append(linacHorizLayout.itemAt(itemIndex).widget())

            for cryomoduleDisplay in cryoDisplayList:
                cmButton: PyDMRelatedDisplayButton = cryomoduleDisplay.children()[1]
                cmButton.setToolTip('cryomodule expert display')

                cmTemplateRepeater: PyDMTemplateRepeater = cryomoduleDisplay.children()[2]

                cryomoduleObject = CRYOMODULE_OBJECTS[str(cmButton.text())]
                cavityWidgetList: List[CavityWidget] = cmTemplateRepeater.findChildren(CavityWidget)

                rfStatusBarList: List[PyDMByteIndicator] = []
                ssaStatusBarList: List[PyDMByteIndicator] = []
                statusBarList = cmTemplateRepeater.findChildren(PyDMByteIndicator)
                for statusBar in statusBarList:
                    if "RFSTATE" in statusBar.accessibleName():
                        rfStatusBarList.append(statusBar)
                    elif "SSA" in statusBar.accessibleName():
                        ssaStatusBarList.append(statusBar)

                for cavityWidget, rfStatusBar, ssaStatusBar in zip(cavityWidgetList, rfStatusBarList, ssaStatusBarList):
                    cavityObject: Cavity = cryomoduleObject.cavities[int(cavityWidget.cavityText)]

                    severityPV: str = (cavityObject.pvPrefix + SEVERITY_SUFFIX)
                    statusPV: str = (cavityObject.pvPrefix + STATUS_SUFFIX)
                    descriptionPV: str = (cavityObject.pvPrefix + DESCRIPTION_SUFFIX)
                    rfStatePV: str = cavityObject.rfStatePV
                    ssaPV: str = cavityObject.ssa.statusPV

                    rfStatusBar.channel = rfStatePV
                    ssaStatusBar.channel = ssaPV

                    cavityWidget.channel = statusPV
                    cavityWidget.severity_channel = severityPV
                    cavityWidget.description_channel = descriptionPV

                    rule = [{"channels": [{"channel": ssaPV, "trigger": True, "use_enum": True}],
                             "property": "Opacity", "expression": "ch[0] == 'SSA On'", "initial_value": "0",
                             "name": "show"}]

                    ssaStatusBar.rules = json.dumps(rule)
