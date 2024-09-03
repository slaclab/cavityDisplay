import pyqtgraph as pg
from PyQt5.QtWidgets import QVBoxLayout, QCheckBox, QPushButton
from pydm import Display


class MakeGui(Display):
    def __init__(self):
        super().__init__()

        main_v_layout = QVBoxLayout()
        self.setLayout(main_v_layout)

        self.pot_checkbox = QCheckBox(text="Check to remove POT fault counts from plot")
        # self.pot_checkbox.stateChanged.connect(self.removePOT)

        self.update_button = QPushButton()
        self.update_button.setText("Update plot")

        self.plot_window = pg.plot()

        main_v_layout.addWidget(self.pot_checkbox)
        main_v_layout.addWidget(self.update_button)
        main_v_layout.addWidget(self.plot_window)

        self.update_button.clicked.connect(self.update_plot)

    def update_plot(self):
        self.plot_window.clear()

        fault_count = [2, 15, 4, 3]

        y_data = ['OFF', 'POT', 'MGT', 'AOT']

        if self.pot_checkbox.isChecked():
            y_data.remove('POT')
            fault_count.remove(15)

        ticks = []
        y_vals_ints = []
        for idy, y_val in enumerate(y_data):
            ticks.append((idy, y_val))
            y_vals_ints.append(idy)

        bargraph = pg.BarGraphItem(x0=0, y=y_vals_ints, height=0.6, width=fault_count, brush='b')
        self.plot_window.addItem(bargraph)

        ax = self.plot_window.getAxis('left')
        ax.setTicks([ticks])
        self.plot_window.showGrid(x=False, y=True, alpha=0.6)

    '''
    def removePOT(self):
        if self.pot_checkbox.isChecked():
            print("Remove POT faults")
            self.pot_checkbox.setText("POT faults removed, uncheck to include them again")
        else:
            print("Not checked")
            self.pot_checkbox.setText("Check to remove POT fault counts from plot")
            
    '''
