from pydm import Display
from PyQt5 import QtGui, QtCore, QtWidgets 
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen 
from PyQt5.QtCore import Qt, QObject
import epics
from epics import caget, caput
from PyQt5.QtWidgets import (QWidgetItem, QCheckBox, QPushButton, QLineEdit,
                             QGroupBox, QHBoxLayout, QMessageBox, QWidget,
                             QLabel, QFrame, QComboBox)
from pydm.widgets import PyDMDrawingRectangle, PyDMLabel
from pydm.widgets.drawing import PyDMDrawingPolygon


class DisplayWithShapes(Display):

	def ui_filename(self):
		return 'DisplayWithShapes.ui'	


	def __init__(self, parent=None, args=None):
		super(DisplayWithShapes, self).__init__(parent=parent, args=args)

		self.ui.embeddedSquare.loadWhenShown = False
		self.ui.embeddedDiamond.loadWhenShown = False
		self.ui.embeddedPolygon.loadWhenShown = False

		#Square
		squareList = self.ui.embeddedSquare.findChildren(PyDMDrawingPolygon)
		squareist = self.ui.embeddedSquare.findChildren(QObject)
#		print(squareist)
		square = squareList[0]
		squareTLCList = self.ui.embeddedSquare.findChildren(PyDMLabel)		
		squareTLC = squareTLCList[0]

		self.ui.makeItGreen(square)
		
		#Diamond		
		diamondList = self.ui.embeddedDiamond.findChildren(PyDMDrawingPolygon)
		diamond = diamondList[0]
		diamondTLCList = self.ui.embeddedDiamond.findChildren(PyDMLabel)
		diamondTLC = diamondTLCList[0]
		self.ui.makeItYellow(diamond)
		
		#Polygon
		polygonList = self.ui.embeddedPolygon.findChildren(PyDMDrawingPolygon)
		print(polygonList)
		polygon = polygonList[0]
		polygonTLCList = self.ui.embeddedPolygon.findChildren(PyDMDrawingPolygon)
		polygonTLC = polygonTLCList[0]
		self.ui.makeItRed(polygon)


		self.ui.EmbeddedCavity.loadWhenShown = False
		rectangleList = self.ui.EmbeddedCavity.findChildren(PyDMDrawingPolygon)
		status = rectangleList[0]
		print(status)
		
		labelList = self.ui.EmbeddedCavity.findChildren(PyDMLabel)
		TLC_label = labelList[0]
#		TLC_label.setText("Fault")
		

		
		# BUTTON CONNECTIONS (send signal and then call a function)
		# Show status of cavity; green if good, yellow if warning
		self.ui.cmGood.shapeBackground = status
		self.ui.cmGood.toggled.connect(lambda:self.makeItGreen(status))

		self.ui.cmWarning.shapeBackground = status
		self.ui.cmWarning.toggled.connect(lambda:self.makeItYellow(status))
		
		self.ui.cmAlarm.shapeBackground = status
		self.ui.cmAlarm.toggled.connect(lambda:self.makeItRed(status))
	
	# change pv value with caput command
	def change_color(self):
		radioButton = self.sender() 	
		self.statusBarColor(radioButton.shapeBackground)

# Change shape color to green
	def makeItGreen(self, shape):
		green = QColor(201,255,203)
		neonGreen = QColor(46,248,10)
		
		shape.brush.setColor(green)
		shape.penColor = neonGreen
		shape.numberOfPoints = 4
		shape.rotation = 45
		shape.update()

# Change shape color to yellow warning
	def makeItYellow(self, shape):
		yellow = QColor(255,253,167)
		neonYellow = QColor(248,228,0)
		
		shape.brush.setColor(yellow)
		shape.penColor = neonYellow
		shape.numberOfPoints = 4
		shape.rotation = 0
		
		shape.update()

# Change shape color to red warning
	def makeItRed(self, shape):
		red = QColor(255,195,187)
		neonRed = QColor(255,0,0)
		
		shape.brush.setColor(red)
		shape.penColor = neonRed
		shape.numberOfPoints = 6
		shape.rotation = 0
		shape.update()


# Change the color of status bar via .setStyleSheet
	def statusBarColor(self, status):
		green = QColor(0,255,0)
		red = QColor(255,54,14)
		Value = caget(self.Test_PV)
		if Value == 1.0:
			status.brush.setColor(green)
			status.update()
		else:
			status.brush.setColor(red)
			status.update()

		
		
