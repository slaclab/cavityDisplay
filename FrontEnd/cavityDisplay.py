from pydm import Display
from PyQt5 import QtGui, QtCore, QtWidgets 
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen 
from PyQt5.QtCore import Qt, QObject
import epics
from epics import caget, caput
from PyQt5.QtWidgets import (QWidgetItem, QPushButton, QGroupBox, QVBoxLayout,
                             QHBoxLayout, QWidget, QLabel, QGridLayout)
from pydm.widgets import PyDMDrawingRectangle, PyDMLabel, PyDMTemplateRepeater, PyDMEmbeddedDisplay
from pydm.widgets.drawing import PyDMDrawingPolygon
from functools import partial
from epics import PV
from frontEnd_constants import shapeParameterDict
from cavityWidget import CavityWidget

import sys
sys.path.insert(0, '..')
from scLinac import LINAC_OBJECTS
from constants import STATUS_SUFFIX, SEVERITY_SUFFIX


class cavityDisplay(Display):

    def ui_filename(self):
        return 'cavityDisplay.ui'   
    
    def __init__(self, parent = None, args = None):
        super(cavityDisplay, self).__init__(parent=parent,args=args)
        
        self.ui.L0B.loadWhenShown = False
        self.ui.L1B.loadWhenShown = False
        self.ui.L2B.loadWhenShown = False
        self.ui.L3B.loadWhenShown = False
        
        embeddedDisplays = [self.ui.L0B,
                            self.ui.L1B,
                            self.ui.L2B,
                            self.ui.L3B] # type: List[PyDMEmbeddedDisplay]
        
        for index, linacEmbeddedDisplay in enumerate(embeddedDisplays):
            linacObject = LINAC_OBJECTS[index]
            print(linacObject.name)
        
            linacHorizLayout = linacEmbeddedDisplay.findChild(QHBoxLayout)
            totalCryos = linacHorizLayout.count()            
            
            # linac will be a list of cryomodules
            linac = []
            for index in range(0,totalCryos):
                linac.append(linacHorizLayout.itemAt(index).widget())

            for cryomodule in linac:
                cmNumber = cryomodule.children()[1]   # cryo number pydmDisplayButton
                cmTemplateRepeater = cryomodule.children()[2] # template repeater of 8 cavities
                
                cryomoduleObject = linacObject.cryomodules[str(cmNumber.text())]
                cavityList = cmTemplateRepeater.findChildren(CavityWidget)
                
                for cavity in cavityList:
                    cavityObject = cryomoduleObject.cavities[int(cavity.cavityText)]
                    
                    severityPV = PV(cavityObject.pvPrefix + SEVERITY_SUFFIX)
                    statusPV = PV(cavityObject.pvPrefix + STATUS_SUFFIX)
                                
                    # This line is meant to initialize the cavity colors and shapes when first launched
                    self.severityCallback(cavity, severityPV.value)
                    self.statusCallback(cavity, statusPV.value)
                    
                    #.add_callback is called when severityPV changes value
                    severityPV.add_callback(partial(self.severityCallback, cavity))
                        
                    #.add_callback is called when statusPV changes value
                    statusPV.add_callback(partial(self.statusCallback, cavity))
                    
                        
        
    # Updates shape depending on pv value
    def severityCallback(self, cavity_widget, value, **kw):
        self.changeShape(cavity_widget, shapeParameterDict[value] if value in shapeParameterDict else shapeParameterDict[3])

    # Change PyDMDrawingPolygon color    
    def changeShape(self, cavity_widget, shapeParameterObject):
        cavity_widget.brush.setColor(shapeParameterObject.fillColor)       
        cavity_widget.penColor = shapeParameterObject.borderColor
        cavity_widget.numberOfPoints = shapeParameterObject.numPoints
        cavity_widget.rotation = shapeParameterObject.rotation
        
    # Change cavity label
    def statusCallback(self, cavity_widget, value, **kw):
        cavity_widget.cavityText = value
