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
    
    print("Hi")    
    
    def __init__(self, parent = None, args = None):
        super(cavityDisplay, self).__init__(parent=parent,args=args)
    
        print("Hi 2.0")        
        embeddedDisplays = [self.ui.L0B,
                            self.ui.L1B,
                            self.ui.L2B,
                            self.ui.L3B] # type: List[PyDMEmbeddedDisplay]
        print("Yo")
        for embeddedDisplay in embeddedDisplays:
            print(embeddedDisplay.children()[0])  # QVBoxLayout
            print(embeddedDisplay.children()[1].text())    # QLabel
            
            print(embeddedDisplay.children()[0].itemAt(0).widget())  #QLabel

            templateRepeater = embeddedDisplay.findChildren(PyDMTemplateRepeater)
            print(templateRepeater)
            templateRepeater.loadWhenShown = False
            
            
            linac = []
            vertLayoutList = templateRepeater.findChildren(QVBoxLayout)
                            
            # PyDMLabel = linac[0].itemAt(0).widget()
            # PyDMTemplateRepeater = linac[0].itemAt(1).widget()
            
            for vertLayout in vertLayoutList:
                templateRepeater = vertLayout.itemAt(1).widget()
                if templateRepeater.accessibleName() == "${cryoTemplate}":
                    linac.append(vertLayout)
            
            for cryomodules in linac:
                cmLabel = cryomodules.itemAt(0).widget()    # cryo number pydmLabel 
                cmTemplateRepeater = cryomodules.itemAt(1).widget()    # templateRepeater of 8 cavities
                
                cryomoduleObject = linacObject.cryomodules[cmLabel.text()]
                
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
