from pydm import Display
from PyQt5 import QtGui, QtCore, QtWidgets 
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen 
from PyQt5.QtCore import Qt, QObject
import epics
from epics import caget, caput
from PyQt5.QtWidgets import (QWidgetItem, QCheckBox, QPushButton, QLineEdit,
                             QGroupBox, QVBoxLayout, QHBoxLayout, QMessageBox, QWidget,
                             QLabel, QFrame, QComboBox, QRadioButton, QGridLayout,
                             QColorDialog)
from pydm.widgets import PyDMDrawingRectangle, PyDMLabel, PyDMTemplateRepeater
from pydm.widgets.drawing import PyDMDrawingPolygon
from functools import partial
from epics import PV
from frontEnd_constants import shapeParameterDict, blackTextColor
from cavityWidget import CavityWidget

import sys
sys.path.insert(0, '..')
from scLinac import LINAC_OBJECTS
from constants import STATUS_SUFFIX, SEVERITY_SUFFIX
from threading import Lock



class cavityDisplay(Display):

    def ui_filename(self):
        return 'cavityDisplay.ui'
        
    def __init__(self, parent = None, args = None):
        super(cavityDisplay, self).__init__(parent=parent,args=args)

        self.mutexDictionary = {}

        self.ui.linac0.loadWhenShown = False
        self.ui.linac1.loadWhenShown = False
        self.ui.linac2.loadWhenShown = False    
        self.ui.linac3.loadWhenShown = False

        repeaters = [self.ui.linac0,
                     self.ui.linac1,
                     self.ui.linac2,
                     self.ui.linac3]  # type: List[PyDMTemplateRepeater]
        
        for index, linacTemplateRepeater in enumerate(repeaters):
            linacObject = LINAC_OBJECTS[index]
            print(linacObject.name)                        
            # PyDMLabel = linac[0].itemAt(0).widget()
            # PyDMTemplateRepeater = linac[0].itemAt(1).widget()
            
            linac = []
            vertLayoutList = linacTemplateRepeater.findChildren(QVBoxLayout)
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
                    self.mutexDictionary[cavity] = Lock()
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
                        
                        
        
    # Updates shape and label depending on pv value
    def severityCallback(self, cavity_widget, value, **kw):
        self.changeShape(cavity_widget, shapeParameterDict[value] if value in shapeParameterDict else shapeParameterDict[3])


    # Change PyDMDrawingPolygon color    
    def changeShape(self, cavity_widget, shapeParameterObject):
        self.mutexDictionary[cavity_widget].acquire()
        cavity_widget.brush.setColor(shapeParameterObject.fillColor)       
        cavity_widget.penColor = shapeParameterObject.borderColor
        cavity_widget.numberOfPoints = shapeParameterObject.numPoints
        cavity_widget.rotation = shapeParameterObject.rotation
        self.mutexDictionary[cavity_widget].release()
        
    # Change cavity label
    def statusCallback(self, cavity_widget, value, **kw):
        self.mutexDictionary[cavity_widget].acquire()
        
        cavity_widget.cavityText = value
        self.mutexDictionary[cavity_widget].release()
