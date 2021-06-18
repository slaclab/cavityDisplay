from pydm import Display
from PyQt5 import QtGui, QtCore, QtWidgets 
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen 
from PyQt5.QtCore import Qt, QObject
import epics
from epics import caget, caput
from PyQt5.QtWidgets import (QWidgetItem, QCheckBox, QPushButton, QLineEdit,
                             QGroupBox, QVBoxLayout, QMessageBox, QWidget,
                             QLabel, QFrame, QComboBox, QRadioButton, QGridLayout,
                             QColorDialog)
from pydm.widgets import PyDMDrawingRectangle, PyDMLabel
from pydm.widgets.drawing import PyDMDrawingPolygon
from functools import partial
from epics import PV

class cryomoduleTemplateRepeater(Display):

	def ui_filename(self):
		return 'cryomoduleTemplateRepeater.ui'
		
	def __init__(self, parent = None, args = None):
		super(cryomoduleTemplateRepeater, self).__init__(parent=parent,args=args)
		
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
		for index, (shape, square) in enumerate (zip(shapeList,squareList)):
			pvList[index].add_callback(partial(self.callback, shape, square, cavityTLCList[index], cavityNumberList[index], value=None))


	def callback(self, shape, square, TLCLabel, CavNumLabel, value, **kw):
		green = QColor(201,255,203)
		neonGreenBorder = QColor(46,248,10)
		
		yellow = QColor(255,253,167)
		neonYellowBorder = QColor(248,228,0)

		red = QColor(255,195,187)
		neonRedBorder = QColor(255,0,0)
		
		blackText = "color: rgba(0,0,0,255); background-color: rgba(0,0,0,0)"
		transparent = "color: rgba(0,0,0,0); background-color: rgba(0,0,0,0)"

		if value<0:
			self.changeSquareColor(square, green, neonGreenBorder)
			self.makeItTransparent(shape)
			TLCLabel.setStyleSheet(transparent)
			CavNumLabel.setStyleSheet(blackText)
		elif value == 0:
			self.makeItTransparent(square)
			self.changeShapeColor(shape, yellow, neonYellowBorder, border=Qt.DotLine, numPoints=4)
			TLCLabel.setStyleSheet(blackText)
			CavNumLabel.setStyleSheet(transparent)
		elif value > 0:
			self.makeItTransparent(square)
			self.changeShapeColor(shape, red, neonRedBorder, border = Qt.DotLine, numPoints=6)
			TLCLabel.setStyleSheet(blackText)
			CavNumLabel.setStyleSheet(transparent)

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
		transparent = QColor(0,0,0,0)
		clearBackground = "background-color: rgba(0,0,0,0)"
		cavShape.setStyleSheet(clearBackground)
		cavShape.brush.setColor(transparent)
		cavShape.penColor = transparent
		cavShape.update()





