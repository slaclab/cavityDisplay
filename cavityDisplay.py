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

from constants import shapeParameterDict
from scLinac import LINACS



class cavityDisplay(Display):

    def ui_filename(self):
        return 'cavityDisplay.ui'
        
    def __init__(self, parent = None, args = None):
        super(cavityDisplay, self).__init__(parent=parent,args=args)

        # What's this for again???????             
        self.ui.linac0.loadWhenShown = False
        self.ui.linac1.loadWhenShown = False
        self.ui.linac2.loadWhenShown = False    
        self.ui.linac3.loadWhenShown = False

        repeaters = [self.ui.linac0,
                     self.ui.linac1,
                     self.ui.linac2,
                     self.ui.linac3]  # type: List[PyDMTemplateRepeater]
        
        for index, linacTemplateRepeater in enumerate(repeaters):
            linacObject = LINACS[index]
            print(linacObject.name)
            linac = linacTemplateRepeater.findChildren(QVBoxLayout)
            
            for cryomodules in linac:
                cmLabel = cryomodules.itemAt(0).widget()    # cryo number pydmLabel 
                cmTemplateRepeater = cryomodules.itemAt(1).widget()    # templateRepeater of 8 cavities
            
                cryomoduleObject = linacObject.cryomodules[cmLabel.text()]
                
                cavityList = cmTemplateRepeater.findChildren(QHBoxLayout)
                
                for cavity in cavityList:
                    cavityWidgetContainer = cavity.itemAt(0).widget()
                    childWidgetsList = cavityWidgetContainer.findChildren(QObject)
                    
                    for childWidget in childWidgetsList:
                        if "cavityLabel" in childWidget.accessibleName():
                            cavityNumberlabel = childWidget
                            cavityNumberlabel.setStyleSheet("background-color: rgba(0,0,0,0)")
                        elif "polygon" in childWidget.accessibleName():
                            polygonShape = childWidget
                        else:
                            print("ERROR in cavity QWidget container")
                    
                    cavityObject = cryomoduleObject.cavities[int(cavityNumberlabel.text())]
                    
                    severityPV = PV(cavityObject.pvPrefix + "CUDSEVR")
                    statusPV = PV(cavityObject.pvPrefix + "CUDSTATUS")
                
                    # This line is meant to initialize the cavity colors and shapes when first launched
                    self.severityCallback(polygonShape, severityPV.value)
                    self.statusCallback(cavityNumberlabel, statusPV.value)
                
                    #.add_callback is called when severityPV changes value
                    severityPV.add_callback(partial(self.severityCallback, polygonShape))
                    
                    #.add_callback is called when statusPV changes value
                    statusPV.add_callback(partial(self.statusCallback, cavityNumberlabel))
                        
                        
        

    # Updates shape and label depending on pv value
    def severityCallback(self, shape, value, **kw):
        self.changeShapeColor(shape, shapeParameterDict[value] if value in shapeParameterDict else shapeParameterDict[3])


    # Change PyDMDrawingPolygon color    
    def changeShapeColor(self, shape, shapeParameterObject):    
        shape.brush.setColor(shapeParameterObject.fillColor)
        shape.penColor = shapeParameterObject.borderColor
        shape.numberOfPoints = shapeParameterObject.numPoints
        shape.rotation = shapeParameterObject.rotation
        shape.update()
        
     # Change cavity label
    def statusCallback(self, cavityLabel, value, **kw):
        cavityLabel.setText(value)

