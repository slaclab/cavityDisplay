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
		pvList = [PV('SIOC:SYS0:ML07:AO011'), PV('SIOC:SYS0:ML07:AO012'), PV('SIOC:SYS0:ML07:AO013'), PV('SIOC:SYS0:ML07:AO014'),PV('SIOC:SYS0:ML07:AO015'),PV('SIOC:SYS0:ML07:AO016'),PV('SIOC:SYS0:ML07:AO017'),PV('SIOC:SYS0:ML07:AO018')]
		
		#self.cav1_PV = PV('SIOC:SYS0:ML07:AO011')
		#self.cav2_PV = 'SIOC:SYS0:ML07:AO012'	
		#self.cav3_PV = 'SIOC:SYS0:ML07:AO013'
		#self.cav4_PV = 'SIOC:SYS0:ML07:AO014'
		#self.cav5_PV = 'SIOC:SYS0:ML07:AO015'
		#self.cav6_PV = 'SIOC:SYS0:ML07:AO016'
		#self.cav7_PV = 'SIOC:SYS0:ML07:AO017'
		#self.cav8_PV = 'SIOC:SYS0:ML07:AO018'
		
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
		for index, grid in enumerate(self.ui.cmTemplate.findChildren(QGridLayout)):
			#goodButton = grid.itemAtPosition(1,1).itemAt(0).widget()
			#warningButton = grid.itemAtPosition(1,1,).itemAt(1).widget()
			#alarmButton = grid.itemAtPosition(1,1).itemAt(2).widget()
			
			#goodButton.toggled.connect(partial(self.changeShapeColor, shape, status = "good"))
			#warningButton.toggled.connect(partial(self.changeShapeColor, shape, status = "warning"))
			#alarmButton.toggled.connect(partial(self.changeShapeColor, shape, status = "alarm"))	
					
			shape = grid.itemAtPosition(1,0).widget()
			print(index, shape)
			
			def callBackFunction(value=None, **kw):
				self.callback(shape,value)
				print(shape, value)
				
			pvList[index].add_callback(callBackFunction)
			


	def callback(self,shape,value):
		#print(shape, value)
		if value<0:
			self.changeShapeColor(shape, "good")
		elif value == 0:
			self.changeShapeColor(shape, "warning")
		elif value > 0:
			self.changeShapeColor(shape, "alarm")

		
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



