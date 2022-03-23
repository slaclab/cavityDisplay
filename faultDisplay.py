from functools import partial
from typing import List

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout
from pydm import Display

from DisplayCavity import DISPLAY_LINAC_OBJECTS
from Fault import Fault, PvInvalid


class FaultDisplay(Display):
    def ui_filename(self):
        # TODO change to real UI file
        return 'frontend/faultDisplay.ui'

    def __init__(self, parent=None, args=None):
        super(FaultDisplay).__init__(parent=parent, args=args)

        for linacObject in DISPLAY_LINAC_OBJECTS:
            for cryomoduleObject in linacObject.cryomodules.values():
                # TODO get cryomodule related display
                pass

                for cavityObject in cryomoduleObject.cavities.values():
                    faults: List[Fault] = cavityObject.faults

                    # TODO this is not correct, I'm making a new Display object here but we want the one that comes out of the related display button
                    cavityFaultWindow = Display(ui_filename=self.getPath("cavityfaultdisplay.ui"),
                                                macros={"cryomodule": cryomoduleObject.name,
                                                        "cavityNumber": cavityObject.number})

                    verticalLayout: QVBoxLayout = cavityFaultWindow.ui.cavityFaultLayout

                    for fault in faults:
                        horizontalLayout = QHBoxLayout()

                        statusLabel = QLabel()

                        codeLabel = QLabel()
                        codeLabel.setText(fault.tlc)

                        nameLabel = QLabel()
                        nameLabel.setText(fault.name)

                        horizontalLayout.addWidget(codeLabel)
                        horizontalLayout.addWidget(nameLabel)
                        horizontalLayout.addWidget(statusLabel)

                        verticalLayout.addWidget(horizontalLayout)

                        fault.pv.add_callback(partial(self.statusLabelCallback, statusLabel, fault))

    @staticmethod
    def statusLabelCallback(label: QLabel, fault: Fault, value, **kw):
        try:
            if fault.isFaulted():
                label.setText("Faulted")
            else:
                label.setText("OK")
        except PvInvalid:
            label.setText("Invalid")
