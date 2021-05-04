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


class Cavities(Display):

	def ui_filename(self):
		return 'Cavities.ui'	


	def __init__(self, parent=None, args=None):
		super(Cavities, self).__init__(parent=parent, args=args)

		self.ui.EmbeddedCavity.loadWhenShown = False
		self.ui.EmbeddedCavity.setStyleSheet("background-color:black\n")
		
		rectangleList = self.ui.EmbeddedCavity.findChildren(PyDMDrawingRectangle)
		statusbar = rectangleList[0]	
		
		labelList = self.ui.EmbeddedCavity.findChildren(PyDMLabel)
		TLC_label = labelList[0]
#		TLC_label.setText("Fault")
		


		# PARAMETERS
		self.PV = ''
		self.Test_PV = 'SIOC:SYS0:ML07:AO010'
		self.value = caget(self.Test_PV)
		
		# BUTTON CONNECTIONS (send signal and then call a function)
		# Show status of cavity; green bar if on frequency (aka PV = 1.0)
		self.ui.cmOFF.PV = self.Test_PV		
		self.ui.cmOFF.value = 0
		self.ui.cmOFF.embeddedStatusbar = statusbar
		self.ui.cmOFF.toggled.connect(self.change_PV)

		self.ui.cmON.PV = self.Test_PV
		self.ui.cmON.value = 1
		self.ui.cmON.embeddedStatusbar = statusbar
		self.ui.cmON.toggled.connect(self.change_PV)


	
	# change pv value with caput command
	def change_PV(self):
		radioButton = self.sender() 
		if radioButton.isChecked():
			caput(radioButton.PV, radioButton.value)	
		self.statusBarColor(radioButton.embeddedStatusbar)
		

# Change the color of status bar via .setStyleSheet
	def statusBarColor(self, statusbar):
		green = QColor(0,255,0)
		red = QColor(255,54,14)
		Value = caget(self.Test_PV)
		if Value == 1.0:
			statusbar.brush.setColor(green)
			statusbar.update()
		else:
			statusbar.brush.setColor(red)
			statusbar.update()

		
		
