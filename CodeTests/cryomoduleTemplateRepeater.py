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
from pydm.widgets import PyDMDrawingRectangle, PyDMLabel
from pydm.widgets.drawing import PyDMDrawingPolygon
from functools import partial
from epics import PV

class cryomoduleTemplateRepeater(Display):

	def ui_filename(self):
		return '../cryomodule.ui'
		
	def __init__(self, parent = None, args = None):
		super(cryomoduleTemplateRepeater, self).__init__(parent=parent,args=args)
		self.defineColors()
		
		# Define PVs for cavities 1 - 8
		pvList = []
		for i in range (1,9):
			pvList.append(PV("SIOC:SYS0:ML07:AO01{cavNum}".format(cavNum=i)))
		
		self.ui.cmTemplate.loadWhenShown = False	
		
		# Read in labels from EmbeddedSingleCavity.ui
		# Make seperate lists for cavity numbers and TLC labels
		cavityNumberList = []
		cavityTLCList = []			
		labelList = self.ui.cmTemplate.findChildren(PyDMLabel)
		for index, items in enumerate (labelList):
			if index%2 == 0:
				cavityTLCList.append(items)
			else:
				cavityNumberList.append(items)

		# Find cavity shapes (square or polygon) in embedded gui
		squareList = self.ui.cmTemplate.findChildren(PyDMDrawingRectangle)
		shapeList = self.ui.cmTemplate.findChildren(PyDMDrawingPolygon)
		
		#Initialize cavity shape colors and label
		for index, (shape, square) in enumerate (zip(shapeList,squareList)):
			pvAlarmStatus = pvList[index].value
			self.callback(shape, square, cavityTLCList[index], cavityNumberList[index], pvAlarmStatus)	

		#.add_callback is called when PV in pvList changes
		for index, (shape, square) in enumerate (zip(shapeList,squareList)):
			pvList[index].add_callback(partial(self.callback, shape, square,
								cavityTLCList[index], cavityNumberList[index], value=None))


	# Updates shape and label depending on pv value
	def callback(self, shape, square, TLCLabel, CavNumLabel, value, **kw):
		if value<0:
			self.changeSquareColor(square, self.green, self.neonGreenBorder)
			self.makeItTransparent(shape)
			TLCLabel.setStyleSheet(self.transparentLabel)
			CavNumLabel.setStyleSheet(self.blackText)
		elif value == 0:
			self.makeItTransparent(square)
			self.changeShapeColor(shape, self.yellow, self.neonYellowBorder, border=Qt.DotLine, numPoints=4)
			TLCLabel.setStyleSheet(self.blackText)
			CavNumLabel.setStyleSheet(self.transparentLabel)
		elif value > 0:
			self.makeItTransparent(square)
			self.changeShapeColor(shape, self.red, self.neonRedBorder, border = Qt.DotLine, numPoints=6)
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
		
		self.blackText = "color: rgba(0,0,0,255); background-color: rgba(0,0,0,0)"
		self.transparentLabel = "color: rgba(0,0,0,0); background-color: rgba(0,0,0,0)"
		
		self.transparentColor = QColor(0,0,0,0)
		self.clearBackground = "background-color: rgba(0,0,0,0)"
		
		
		
