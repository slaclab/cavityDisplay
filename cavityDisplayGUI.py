import json
import sys
from dataclasses import dataclass
from functools import partial
from typing import List

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QHBoxLayout, QWidget
from epics import caget, camonitor
from numpy import array2string, ndarray
from pydm import Display
from pydm.widgets import (PyDMByteIndicator, PyDMDrawingLine, PyDMEmbeddedDisplay, PyDMRelatedDisplayButton,
                          PyDMTemplateRepeater)

from lcls_tools.superconducting.scLinac import CRYOMODULE_OBJECTS, Cavity

sys.path.insert(0, './frontend')
from cavityWidget import CavityWidget

STATUS_SUFFIX = "CUDSTATUS"
SEVERITY_SUFFIX = "CUDSEVR"
DESCRIPTION_SUFFIX = "CUDDESC"
RF_STATUS_SUFFIX = "RFSTATE"

GREEN_FILL_COLOR = QColor(9, 141, 0)
YELLOW_FILL_COLOR = QColor(244, 230, 67)
RED_FILL_COLOR = QColor(150, 0, 0)
PURPLE_FILL_COLOR = QColor(131, 61, 235)
GRAY_FILL_COLOR = QColor(127, 127, 127)
BLUE_FILL_COLOR = QColor(14, 191, 255)
LIMEGREEN_FILL_COLOR = QColor(92, 253, 92)

BLACK_TEXT_COLOR = QColor(0, 0, 0)
DARK_GRAY_COLOR = QColor(40, 40, 40)
WHITE_TEXT_COLOR = QColor(250, 250, 250)


@dataclass
class ShapeParameters:
    fillColor: QColor
    borderColor: QColor
    numPoints: int
    rotation: float


SHAPE_PARAMETER_DICT = {0: ShapeParameters(GREEN_FILL_COLOR, GREEN_FILL_COLOR,
                                           4, 0),
                        1: ShapeParameters(YELLOW_FILL_COLOR, YELLOW_FILL_COLOR,
                                           3, 0),
                        2: ShapeParameters(RED_FILL_COLOR, RED_FILL_COLOR,
                                           6, 0),
                        3: ShapeParameters(PURPLE_FILL_COLOR, PURPLE_FILL_COLOR,
                                           20, 0),
                        4: ShapeParameters(GRAY_FILL_COLOR, GRAY_FILL_COLOR,
                                           10, 0)}


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
                    
                    rule = [{"channels": [{"channel": ssaPV, "trigger": True, "use_enum": True}],
                             "property": "Visible", "expression": "ch[0] == 'SSA On'", "initial_value": "True",
                             "name"    : "show"}]
                    
                    ssaStatusBar.rules = json.dumps(rule)
                    
                    # These lines are meant to initialize the cavityWidget color, shape, and descriptionPV values
                    # when first launched. If we don't initialize the description PV, it would remain empty
                    # until the pv value changes
                    self.severityCallback(cavityWidget, caget(severityPV))
                    # self.statusCallback(cavityWidget, caget(statusPV))
                    self.descriptionCallback(cavityWidget, caget(descriptionPV))
                    # self.rfStatusCallback(rfStatusBar, caget(rfStatePV, timeout=0.1))
                    # self.ssaStatusCallback(ssaStatusBar, caget(ssaPV))
                    
                    # .add_callback is called when severityPV changes value
                    camonitor(severityPV, partial(self.severityCallback, cavityWidget))
                    
                    # .add_callback is called when statusPV changes value
                    # camonitor(statusPV, partial(self.statusCallback, cavityWidget))
                    
                    # .add_callback is called when descriptionPV changes value
                    camonitor(descriptionPV, partial(self.descriptionCallback, cavityWidget))
                    
                    # .add_callback is called when rfStatePV changes value
                    # camonitor(rfStatePV, partial(self.rfStatusCallback, rfStatusBar))
                    
                    # .add_callback is called when ssaStatePV changes value
                    # camonitor(ssaPV, partial(self.ssaStatusCallback, ssaStatusBar))
    
    # A blue line appears under the cavity if the RF is on
    @staticmethod
    def rfStatusCallback(rf_StatusBar: PyDMDrawingLine, value: int, **kw):
        if value == 1:
            rf_StatusBar.penColor = BLUE_FILL_COLOR
            rf_StatusBar.setToolTip("RF on")
        elif value == 0:
            rf_StatusBar.penColor = DARK_GRAY_COLOR
            rf_StatusBar.setToolTip("RF off")
        else:
            print("RFSTATE pv value is not On or Off, nor disconnected")
        rf_StatusBar.update()
    
    # An orange line appears under the cavity if its SSA is on
    @staticmethod
    def ssaStatusCallback(ssa_StatusBar: PyDMDrawingLine, value: int, **kw):
        if value == 3:
            ssa_StatusBar.penColor = LIMEGREEN_FILL_COLOR
            ssa_StatusBar.setToolTip("SSA on")
        elif value != 3:
            ssa_StatusBar.penColor = DARK_GRAY_COLOR
            ssa_StatusBar.setToolTip("SSA off")
        ssa_StatusBar.update()
    
    # Updates shape depending on pv value
    def severityCallback(self, cavity_widget: CavityWidget, value: int, **kw):
        self.changeShape(cavity_widget,
                         SHAPE_PARAMETER_DICT[value]
                         if value in SHAPE_PARAMETER_DICT
                         else SHAPE_PARAMETER_DICT[3])
    
    # Change the hover text of each cavity to show a description for the tlc fault
    @staticmethod
    def descriptionCallback(cavity_widget: QWidget, value: ndarray, **kw):
        if isinstance(value, str):
            cavity_widget.setToolTip(value)
        else:
            shortFaultDescription = array2string(value)
            cavity_widget.setToolTip(shortFaultDescription)
    
    # Change PyDMDrawingPolygon color
    @staticmethod
    def changeShape(cavity_widget, shapeParameterObject):
        cavity_widget.brush.setColor(shapeParameterObject.fillColor)
        cavity_widget.penColor = shapeParameterObject.borderColor
        cavity_widget.numberOfPoints = shapeParameterObject.numPoints
        cavity_widget.rotation = shapeParameterObject.rotation
    
    # Change cavity label
    @staticmethod
    def statusCallback(cavity_widget, value, **kw):
        cavity_widget.cavityText = value
        cavity_widget.update()
