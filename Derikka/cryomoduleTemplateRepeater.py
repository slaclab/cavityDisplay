from pydm import Display
from PyQt5 import QtGui, QtCore, QtWidgets 
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen 
from PyQt5.QtCore import Qt, QObject
import epics
from epics import caget, caput
from PyQt5.QtWidgets import (QWidgetItem, QCheckBox, QPushButton, QLineEdit,
                             QGroupBox, QVBoxLayout, QMessageBox, QWidget,
                             QLabel, QFrame, QComboBox, QRadioButton, QGridLayout)
from pydm.widgets import PyDMDrawingRectangle, PyDMLabel
from pydm.widgets.drawing import PyDMDrawingPolygon

class cryomoduleTemplateRepeater(Display):

	def ui_filename(self):
		return 'cryomoduleTemplateRepeater.ui'
		
	def __init__(self, parent = None, args = None):
		super(cryomoduleTemplateRepeater, self).__init__(parent=parent,args=args)
		
		self.ui.cmTemplate.loadWhenShown = False
		
		# --- Read in drawing object and labels from EmbeddedSingleCavity.ui ---
		shapeList = self.ui.cmTemplate.findChildren(PyDMDrawingPolygon)
		
		# Make seperate lists for cavity numbers and TLC
		cavityNumberList = []
		cavityTLCList = []
			
		labelList = self.ui.cmTemplate.findChildren(PyDMLabel)
		for index, items in enumerate (labelList):
			if index%2 == 0:
				cavityNumberList.append(items)
			else:
				cavityTLCList.append(items)

		for grid in self.ui.cmTemplate.findChildren(QGridLayout):
			print(grid)
		
		# BUTTON CONNECTIONS
		#def setupButtons(self):
#		name2button = {} # type: Dict[str: QRadioButton]

		# Grab radio buttons from template repeater and 
		# name them according to cavities.json via accessible names
#		for button in self.ui.cmTemplate.findChildren(QRadioButton):
#			name2button[button.accessibleName()]= button #Fill the dictionary
#		print (name2button)
#		name2button["Good"].toggled.connect(lambda:self.makeItGreen(shapeList[0]))

#		radioButtonsList = self.ui.cmTemplate.findChildren(QRadioButton)
#		for index, button in enumerate (radioButtonsList):
#			if index%3 == 0:
#				print(index, index%3,button,shapeList[index])
#				button.toggled.connect(lambda:self.makeItGreen(shapeList[index]))
#			if index%3 == 1:
#				print(index, index%3,button,shapeList[index])
#				button.toggled.connect(lambda:self.makeItYellow(shapeList[index]))
#			if index%3 == 2:
#				print(index, index%3,button,shapeList[index])
#				button.toggled.connect(lambda:self.makeItYellow(shapeList[index]))
		
		
#		GoodButton1 = radioButtonsList[0]
#		GoodButton1.toggled.connect(lambda:self.makeItGreen(shapeList[0]))
		
#		WarningButton1 = radioButtonsList[1]
#		WarningButton1.toggled.connect(lambda:self.makeItYellow(shapeList[0]))

#		AlarmButton1 = radioButtonsList[2]
#		AlarmButton1.toggled.connect(lambda:self.makeItRed(shapeList[0]))

			
		
		
		# Practice changing a cavity shape color
#		self.makeItRed(shapeList[0])
#		self.makeItYellow(shapeList[2])
#		self.makeItGreen(shapeList[4])

# Change shape color to yellow warning
	def makeItYellow(self, shape):
		yellow = QColor(255,253,167)
		neonYellow = QColor(248,228,0)
		
		shape.brush.setColor(yellow)
		shape.penColor = neonYellow
		shape.numberOfPoints = 3
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

# Change shape color to green
	def makeItGreen(self, shape):
		green = QColor(201,255,203)
		neonGreen = QColor(46,248,10)
		
		shape.brush.setColor(green)
		shape.penColor = neonGreen
		shape.numberOfPoints = 4
		shape.rotation = 0
		shape.update()

