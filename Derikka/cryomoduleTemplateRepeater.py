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
from epics import PV

class cryomoduleTemplateRepeater(Display):

	def ui_filename(self):
		return 'cryomoduleTemplateRepeater.ui'
		
	def __init__(self, parent = None, args = None):
		super(cryomoduleTemplateRepeater, self).__init__(parent=parent,args=args)
		
		# Define PVs for cavities 1 - 8
		pvList = [PV('SIOC:SYS0:ML07:AO011'), PV('SIOC:SYS0:ML07:AO012'), 
			PV('SIOC:SYS0:ML07:AO013'), PV('SIOC:SYS0:ML07:AO014'),
			PV('SIOC:SYS0:ML07:AO015'),PV('SIOC:SYS0:ML07:AO016'),
			PV('SIOC:SYS0:ML07:AO017'),PV('SIOC:SYS0:ML07:AO018')]
		
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

		# Find specific objects based on their location in single cavity's vertical layout
		for index, vLayout in enumerate(self.ui.cmTemplate.findChildren(QVBoxLayout)):
			if index == 0:
				pass
			else:
				shape = vLayout.itemAt(1).widget()
				pvList[index-1].add_callback(partial(self.callback, shape, value=None))
				

	def callback(self,shape,value, **kw):
		green = QColor(201,255,203)
		neonGreenBorder = QColor(46,248,10)
		
		yellow = QColor(255,253,167)
		neonYellowBorder = QColor(248,228,0)

		red = QColor(255,195,187)
		neonRedBorder = QColor(255,0,0)

		if value<0:
			self.changeShapeColor(shape, green, neonGreenBorder, numPoints=4)
		elif value == 0:
			self.changeShapeColor(shape, yellow, neonYellowBorder, numPoints=3)
		elif value > 0:
			self.changeShapeColor(shape, red, neonRedBorder, numPoints=6)

		
	def changeShapeColor(self, shape, fillColor, borderColor, numPoints):
		shape.brush.setColor(fillColor)
		shape.penColor = borderColor
		shape.numberOfPoints = numPoints
		shape.rotation = 0
		
		shape.update()




