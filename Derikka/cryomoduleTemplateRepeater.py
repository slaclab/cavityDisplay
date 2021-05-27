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
from functools import partial

class cryomoduleTemplateRepeater(Display):

	def ui_filename(self):
		return 'cryomoduleTemplateRepeater.ui'
		
	def __init__(self, parent = None, args = None):
		super(cryomoduleTemplateRepeater, self).__init__(parent=parent,args=args)
		
		self.ui.cmTemplate.loadWhenShown = False
		
		# Read in labels from EmbeddedSingleCavity.ui
		# Make seperate lists for cavity numbers and TLC labels
		cavityNumberList = []
		cavityTLCList = []			
		labelList = self.ui.cmTemplate.findChildren(PyDMLabel)
		for index, items in enumerate (labelList):
			if index%2 == 0:
				cavityNumberList.append(items)
			else:
				cavityTLCList.append(items)

		# Find specific objects based on their location in single cavity's grid layout
		for grid in self.ui.cmTemplate.findChildren(QGridLayout):
			goodButton = grid.itemAtPosition(1,1).itemAt(0).widget()
			warningButton = grid.itemAtPosition(1,1,).itemAt(1).widget()
			alarmButton = grid.itemAtPosition(1,1).itemAt(2).widget()
			
			shape = grid.itemAtPosition(1,0).widget()
			
			goodButton.toggled.connect(partial(self.changeShapeColor, shape, status = "good"))
			warningButton.toggled.connect(partial(self.changeShapeColor, shape, status = "warning"))
			alarmButton.toggled.connect(partial(self.changeShapeColor, shape, status = "alarm"))
		


	def changeShapeColor(self, shape, status):
		green = QColor(201,255,203)
		neonGreenBorder = QColor(46,248,10)
		
		yellow = QColor(255,253,167)
		neonYellowBorder = QColor(248,228,0)

		red = QColor(255,195,187)
		neonRedBorder = QColor(255,0,0)
		
		if (status == "good"):
			shape.brush.setColor(green)
			shape.penColor = neonGreenBorder
			shape.numberOfPoints = 4
			shape.rotation = 0
		elif (status == "warning"):
			shape.brush.setColor(yellow)
			shape.penColor = neonYellowBorder
			shape.numberOfPoints = 3
			shape.rotation = 0
		elif (status == "alarm"):
			shape.brush.setColor(red)
			shape.penColor = neonRedBorder
			shape.numberOfPoints = 6
			shape.rotation = 0
			
		shape.update()



