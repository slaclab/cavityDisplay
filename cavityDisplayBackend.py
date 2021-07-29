from constants import *

class Fault:
	def __init__(self, severity, tlc, pv, color):
		self.severity = severity
		self.tlc = tlc
		self.pv = pv
		self.color = color
		
	def __gt__(self, other):
		return self.severity > other.severity


faults = {}
faults = {"ARU": Fault(severity = 1, tlc = "ARU", pv = None, color = "R")}
print(faults["ARU"])


'''
class Fault:
	def __init__(self, severity, tlc, pv, color):
		self.severity = severity
		self.tlc = tlc
		self.pv = pv
		self.color = color

faults = {}
faults = {"ARU": Fault(severity=1, tlc="ARU", pv=None, color="R")}

print(faults) #{'ARU': <__main__.Fault instance at 0x7f1bfeee81b8>}

f = faults["ARU"]

print(f) # <__main__.Fault instance at 0x7f1bfeee81b8>

print(f.color) # 'R'
'''
