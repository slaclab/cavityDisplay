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
							if "TLC" in childWidget.accessibleName():
								cavityTLClabel = childWidget
							elif "cavityNumber" in childWidget.accessibleName():
								cavityNumberlabel = childWidget
							elif "square" in childWidget.accessibleName():
								squareShape = childWidget
							elif "polygon" in childWidget.accessibleName():
								polygonShape = childWidget
							else:
								print("ERROR in cavity QWidget container")
							
						statusPVstring = "ACCL:{LINAC}:{CRYOMODULE_NUM}{CAVITY}0:CUDSEVR".format(LINAC = linacTemplateRepeater.accessibleName(),
																			CRYOMODULE_NUM = cmLabel.text(),
																			CAVITY = cavityNumberlabel.text())
						statusPV = PV(statusPVstring)
					
						# This line is meant to initialize the cavity colors and shapes when first launched
						self.Severitycallback(polygonShape, squareShape, cavityTLClabel, cavityNumberlabel, statusPV.value)
					
						#.add_callback is called when statusPV changes value
						statusPV.add_callback(partial(self.Severitycallback, polygonShape, squareShape,
										cavityTLClabel, cavityNumberlabel))
		

	# Updates shape and label depending on pv value
	def Severitycallback(self, shape, square, TLCLabel, CavNumLabel, value, **kw):
		if value==0:
			# Make it green
			self.changeSquareColor(square, self.green, self.neonGreenBorder)
			self.makeItTransparent(shape)
			TLCLabel.setStyleSheet(self.transparentLabel)
			CavNumLabel.setStyleSheet(self.blackText)
		elif value==1:
			# Make it yellow
			self.makeItTransparent(square)
			self.changeShapeColor(shape, self.yellow, self.neonYellowBorder, border=Qt.DotLine, numPoints=4)
			TLCLabel.setStyleSheet(self.blackText)
			CavNumLabel.setStyleSheet(self.transparentLabel)
		elif value==2:
			# Make it red
			self.makeItTransparent(square)
			self.changeShapeColor(shape, self.red, self.neonRedBorder, border = Qt.DotLine, numPoints=6)
			TLCLabel.setStyleSheet(self.blackText)
			CavNumLabel.setStyleSheet(self.transparentLabel)
		else:
			# Make it purple
			self.makeItTransparent(square)
			self.changeShapeColor(shape, self.purple, self.neonPurpleBorder, border = Qt.DotLine, numPoints=6)
			TLCLabel.setStyleSheet(self.blackText)
			CavNumLabel.setStyleSheet(self.transparentLabel)


	# Change PyDMDrawingPolygon color	
	def changeShapeColor(self, shape, fillColor, borderColor, border, numPoints):	
		shape.brush.setColor(fillColor)
		shape.penColor = borderColor
		shape.numberOfPoints = numPoints
		shape.penStyle = border
		shape.update()
	
	# Change PyDMDrawingRectangle color
	def changeSquareColor(self, square, fillColor, borderColor):
		square.brush.setColor(fillColor)
		square.penColor = borderColor
		square.update()
	
	# Make PyDMDrawingRectangle or Polygon transparent via alpha = 0 in rgba	
	def makeItTransparent(self, cavShape):
		cavShape.setStyleSheet(self.clearBackground)
		cavShape.brush.setColor(self.transparentColor)
		cavShape.penColor = self.transparentColor
		cavShape.update()


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
		
		self.blackText = "color: rgba(0,0,0,255); background-color: rgba(0,0,0,0)"
		self.transparentLabel = "color: rgba(0,0,0,0); background-color: rgba(0,0,0,0)"
		
		self.transparentColor = QColor(0,0,0,0)
		self.clearBackground = "background-color: rgba(0,0,0,0)"
		

