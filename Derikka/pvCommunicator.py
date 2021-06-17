from pydm import Display
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import (QWidgetItem, QCheckBox, QPushButton, QLineEdit,
                             QGroupBox, QVBoxLayout, QMessageBox, QWidget,
                             QLabel, QFrame, QComboBox, QRadioButton, QGridLayout,
                             QColorDialog)
from pydm.widgets import PyDMDrawingRectangle, PyDMLabel
import epics
from epics import caget, caput
from functools import partial


class pvCommunicator(Display):
	
	def __init__(self, parent=None, args=None):
		super(pvCommunicator, self).__init__(parent=parent, args=args)
		self.connectElements()
		
	def ui_filename(self):
		return 'pvCommunicator.ui'

	# Function associates specific PV with each corresponding QLineEdit Object
	# Then establishes connection to readValue() function when user enters a value
	def connectElements(self):
		self.ui.inputPV1.PV = 'SIOC:SYS0:ML07:AO011'
		self.ui.inputPV1.returnPressed.connect(lambda:self.readValue())

		self.ui.inputPV2.PV = 'SIOC:SYS0:ML07:AO012'
		self.ui.inputPV2.returnPressed.connect(lambda:self.readValue())

		self.ui.inputPV3.PV = 'SIOC:SYS0:ML07:AO013'
		self.ui.inputPV3.returnPressed.connect(lambda:self.readValue())

		self.ui.inputPV4.PV = 'SIOC:SYS0:ML07:AO014'
		self.ui.inputPV4.returnPressed.connect(lambda:self.readValue())

		self.ui.inputPV5.PV = 'SIOC:SYS0:ML07:AO015'
		self.ui.inputPV5.returnPressed.connect(lambda:self.readValue())

		self.ui.inputPV6.PV = 'SIOC:SYS0:ML07:AO016'
		self.ui.inputPV6.returnPressed.connect(lambda:self.readValue())

		self.ui.inputPV7.PV = 'SIOC:SYS0:ML07:AO017'
		self.ui.inputPV7.returnPressed.connect(lambda:self.readValue())

		self.ui.inputPV8.PV = 'SIOC:SYS0:ML07:AO018'
		self.ui.inputPV8.returnPressed.connect(lambda:self.readValue())

	
	# self.sender() identifies which QLineEdit object was typed into
	# changes PV value to corresponding user input	
	def readValue(self):
		lineInfo = self.sender()
		userInput = lineInfo.text()
		print(userInput)
		caput(lineInfo.PV, userInput)


