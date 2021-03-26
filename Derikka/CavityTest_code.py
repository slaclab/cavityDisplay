from pydm import Display
from PyQt5 import QtGui, QtCore, QtWidgets
import epics
from epics import caget, caput


class CavityTest(Display):
	
	def __init__(self, parent=None, args=None):
		super(CavityTest, self).__init__(parent=parent, args=args)

		self.ui.testButton.clicked.connect(lambda:self.updatePVOutput("Button Pushed, PV = " + str(caget('SIOC:SYS0:ML07:AO010'))))		
		pvValue = caget('SIOC:SYS0:ML07:AO010')   # Read value of pv		

		self.ui.testCheckBox.stateChanged.connect(self.buttonToggled)

	def ui_filename(self):
		return 'CavityTest.ui'
		
	def updateOutput(self, output):
		print(output)
		self.ui.outputBox.setText(output)

	def updatePVOutput(self, output):
		print(output)
		self.ui.pvOutput.setText(output)

	# Check and uncheck the checkbox to set the PV to a new value
	def buttonToggled(self):
		if self.ui.testCheckBox.isChecked():
			new = 0.0
			caput('SIOC:SYS0:ML07:AO010', new)
			self.ui.outputBox.setText("Checkbox is checked. Setting PV to 0")
		else:
			new = 1.0
			caput('SIOC:SYS0:ML07:AO010', new)			
			self.ui.outputBox.setText("Checkbox is not checked. Setting PV to 1")
			
	
	
	


