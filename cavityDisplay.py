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

class cavityDisplay(Display):

	def ui_filename(self):
		return 'cavityDisplay.ui'
		
	def __init__(self, parent = None, args = None):
		super(cavityDisplay, self).__init__(parent=parent,args=args)
		self.defineColors()

		# What's this for again??????? 			
		self.ui.linac0.loadWhenShown = False
		self.ui.linac1.loadWhenShown = False
		self.ui.linac2.loadWhenShown = False	
		self.ui.linac3.loadWhenShown = False

		repeaters = [self.ui.linac0,
                     self.ui.linac1,
                     self.ui.linac2,
                     self.ui.linac3]  # type: List[PyDMTemplateRepeater]
		
		for linacTemplateRepeater in repeaters:
			print(linacTemplateRepeater.accessibleName())
			linac = linacTemplateRepeater.findChildren(QVBoxLayout)
			
			for cryomodules in linac:
				cmLabel = cryomodules.itemAt(0).widget()	# cryo number pydmLabel 
				cmTemplateRepeater = cryomodules.itemAt(1).widget()	# templateRepeater of 8 cavities
				
				if "cryomoduleName" in cmLabel.accessibleName():
					cavityList = cmTemplateRepeater.findChildren(QHBoxLayout)

					for i, cavity in enumerate(cavityList):
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
							
						statusPVstring = "ACCL:{LINAC}:{CRYOMODULE_NUM}{CAVITY}0:CUDSEVR".format(LINAC = linacTemplateRepeater.accessibleName(),
																			CRYOMODULE_NUM = cmLabel.text(),
																			CAVITY = cavityNumberlabel.text())
						statusPV = PV(statusPVstring)
					
						# This line is meant to initialize the cavity colors and shapes when first launched
						self.Severitycallback(polygonShape, cavityNumberlabel, statusPV.value)
					
						#.add_callback is called when statusPV changes value
						statusPV.add_callback(partial(self.Severitycallback, polygonShape,
										cavityNumberlabel))
		

	# Updates shape and label depending on pv value
	def Severitycallback(self, shape, CavNumLabel, value, **kw):
		if value==0:
			# Make it green
			self.changeShapeColor(shape, self.green, self.neonGreenBorder, border=Qt.SolidLine, numPoints=4, rotation=45)
		elif value==1:
			# Make it yellow
			self.changeShapeColor(shape, self.yellow, self.neonYellowBorder, border=Qt.DotLine, numPoints=4,rotation=0)
		elif value==2:
			# Make it red
			self.changeShapeColor(shape, self.red, self.neonRedBorder, border = Qt.DotLine, numPoints=6,rotation=0)
		else:
			# Make it purple
			self.changeShapeColor(shape, self.purple, self.neonPurpleBorder, border = Qt.DotLine, numPoints=20,rotation=0)


	# Change PyDMDrawingPolygon color	
	def changeShapeColor(self, shape, fillColor, borderColor, border, numPoints,rotation):	
		shape.brush.setColor(fillColor)
		shape.penColor = borderColor
		shape.numberOfPoints = numPoints
		shape.penStyle = border
		shape.rotation = rotation
		shape.update()


	# Define all colors to be used in GUI
	def defineColors(self):
		self.green = QColor(201,255,203)
		self.neonGreenBorder = QColor(46,248,10)
		
		self.yellow = QColor(255,253,167)
		self.neonYellowBorder = QColor(248,228,0)

		self.red = QColor(255,195,187)
		self.neonRedBorder = QColor(255,0,0)
		
		self.purple = QColor(209,203,255)
		self.neonPurpleBorder = QColor(170,85,255)
		
		

