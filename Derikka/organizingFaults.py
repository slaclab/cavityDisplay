# 1. Get information on faults and orgnize the data into a list
# 2. (todo) sort numbers in preparation for sorting alarms by severity

# This class can reference the value, TLC, and severity of a fault
class faultSeverity:
	def __init__(self, value, TLC, severity):
		self.value = value
		self.TLC = TLC
		self.severity = severity

# Initialize list of faults 	
ARU = faultSeverity(1, 'ARU', 1)
MNT = faultSeverity(1, 'MNT', 2)
HWI = faultSeverity(1, 'HWI', 3)
PHJ = faultSeverity(1, 'PHJ', 4)


# Add faults to a list
faultList = []
faultList.append(ARU)
faultList.append(MNT)
faultList.append(HWI)
faultList.append(PHJ)

for elements in faultList:
	print(elements.TLC, elements.severity)
	
displayList = []
for elements in faultList:
	displayList.append(elements.severity)

displayList.sort()
print(displayList)
#print('Display List sorted: ', displayList)
	
	
print("----------Dictionary --------------------")
# Adding faults to a dict
faults = {}
faults['aru'] = {'Value': 1, 'TLC':'ARU', 'Severity': 1}
faults['mnt'] = {'Value': 1, 'TLC':'MNT', 'Severity': 2}
faults['hwi'] = {'Value': 1, 'TLC':'HWI', 'Severity': 3}
faults['phj'] = {'Value': 1, 'TLC':'PHJ', 'Severity': 4}

#print( faults['phj']['TLC'] )
for elements in faults:
	print(elements, faults[elements]['TLC'], faults[elements]['Severity'])
	
print(sorted(faults.items(), key=faults.get() ))


displayList = []
	







	
