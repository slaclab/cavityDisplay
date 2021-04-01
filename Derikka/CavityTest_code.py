from pydm import Display
from PyQt5 import QtGui, QtCore, QtWidgets
import epics
from epics import caget, caput

class CavityTest(Display):

	def ui_filename(self):
		return 'CavityTest.ui'	

	def __init__(self, parent=None, args=None):
		super(CavityTest, self).__init__(parent=parent, args=args)

		# Parameters
		self.PV = ''									# current PV
		self.Test_PV = 'SIOC:SYS0:ML07:AO010'			# PV string
		self.value = caget(self.Test_PV)				

		# Button Connections (send signal and then call a function)
		self.ui.Qt_pvPushButton.clicked.connect(lambda:self.updatePVOutput())				

		self.ui.Qt_radioButton0.PV = self.Test_PV		
		self.ui.Qt_radioButton0.value = 0
		self.ui.Qt_radioButton0.toggled.connect(self.change_PV)

		self.ui.Qt_radioButton1.PV = self.Test_PV
		self.ui.Qt_radioButton1.value = 1
		self.ui.Qt_radioButton1.toggled.connect(self.change_PV)	
		

	# change pv value with caput command
	def change_PV(self):
		# self.sender() identifies object that triggered event (i.e. which radio button was pressed)
		radioButton = self.sender() 
		if radioButton.isChecked():
			caput(radioButton.PV, radioButton.value)					# Use radioButton.PV in place of 'SIOC:SYS0:ML07:AO010'
			self.ui.Qt_radioOutput.setText("Radio button toggled to PV value of " + str(radioButton.value) )					
	
		print("Terminal Text: Radio Button pressed " + str(radioButton.value) )		

		self.colorChange()
			
	# Update text output associated with Display PV Value PushButton
	def updatePVOutput(self):
		output = "Button Pushed, PV = " + str(caget(self.Test_PV))		
		self.ui.Qt_pvOutput.setText(output)
	
		print("Terminal Text: " + str(output))
	
	# Change the color of something via .setStyleSheet depending on its value
	def colorChange(self):
		self.text = "color: rgb(50,50,50);"
		self.green = "background-color: rgb(153, 255, 148);\n"
		self.red = "background-color: rgb(255,92,92);\n"

		Value = caget(self.Test_PV)
		if Value == 1.0:
			self.ui.label_CM01.setStyleSheet( str(self.text) + str(self.green) )
		else:
			self.ui.label_CM01.setStyleSheet( str(self.text) + str(self.red) )	
	
			print("Terminal Text: We're in the colorChange function!")
			
	
	
	


