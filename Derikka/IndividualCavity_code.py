from pydm import Display
from PyQt5 import QtGui, QtCore, QtWidgets #, QPainter (Why this not work?) 
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen
from PyQt5.QtCore import Qt
import epics
from epics import caget, caput


class IndividualCavity(Display):

	def ui_filename(self):
		return 'IndividualCavity.ui'	


	def __init__(self, parent=None, args=None):
		super(IndividualCavity, self).__init__(parent=parent, args=args)
		
		# PARAMETERS
		self.PV = ''
		self.Test_PV = 'SIOC:SYS0:ML07:AO010'
		self.value = caget(self.Test_PV)
		
		# BUTTON CONNECTIONS (send signal and then call a function)
		# Show status of cavity; green bar if on frequency (aka PV = 1.0)
		self.ui.cmOFF.PV = self.Test_PV		
		self.ui.cmOFF.value = 0
		self.ui.cmOFF.toggled.connect(self.change_PV)

		self.ui.cmON.PV = self.Test_PV
		self.ui.cmON.value = 1
		self.ui.cmON.toggled.connect(self.change_PV)

#		self.statusBarColor()

	
	# change pv value with caput command
	def change_PV(self):
		radioButton = self.sender() 
		if radioButton.isChecked():
			caput(radioButton.PV, radioButton.value)	
		self.statusBarColor()
		

# Change the color of status bar via .setStyleSheet
	def statusBarColor(self):
		green = QColor(0,255,0)
		red = QColor(255,54,14)
		Value = caget(self.Test_PV)
		if Value == 1.0:
			self.ui.CavityStatusBar.brush.setColor(green)
			self.ui.CavityStatusBar.update()
		else:
			self.ui.CavityStatusBar.brush.setColor(red)
			self.ui.CavityStatusBar.update()

		
		
