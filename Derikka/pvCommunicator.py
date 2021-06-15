from pydm import Display
from PyQt5 import QtGui, QtCore, QtWidgets
import epics
from epics import caget, caput


class pvCommunicator(Display):
	
	def __init__(self, parent=None, args=None):
		super(pvCommunicator, self).__init__(parent=parent, args=args)
		self.connectElements()
		
	def ui_filename(self):
		return 'pvCommunicator.ui'
		
	def connectElements(self):
		self.inputPV1.returnPressed.connect(lambda:self.changeValue('SIOC:SYS0:ML07:AO011'))
		self.inputPV2.returnPressed.connect(lambda:self.changeValue('SIOC:SYS0:ML07:AO012'))
		self.inputPV3.returnPressed.connect(lambda:self.changeValue('SIOC:SYS0:ML07:AO013'))
		self.inputPV4.returnPressed.connect(lambda:self.changeValue('SIOC:SYS0:ML07:AO014'))
		self.inputPV5.returnPressed.connect(lambda:self.changeValue('SIOC:SYS0:ML07:AO015'))
		self.inputPV6.returnPressed.connect(lambda:self.changeValue('SIOC:SYS0:ML07:AO016'))
		self.inputPV7.returnPressed.connect(lambda:self.changeValue('SIOC:SYS0:ML07:AO017'))
		self.inputPV2.returnPressed.connect(lambda:self.changeValue('SIOC:SYS0:ML07:AO018'))
		
	def changeValue(self,pv_name):
		newValue = self.inputPV1.text()
		caput(pv_name, newValue)
		print newValue
