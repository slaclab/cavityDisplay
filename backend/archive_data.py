import pyqtgraph as pg
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QComboBox, QDateTimeEdit, QPushButton, QLabel
from pydm import Display
from typing import Dict

from backend.backend_cavity import BackendCavity
from lcls_tools.superconducting.sc_linac import Machine
from lcls_tools.superconducting.sc_linac_utils import ALL_CRYOMODULES

DISPLAY_MACHINE = Machine(cavity_class=BackendCavity)


class FaultCounter(Display):
    def __init__(self):
        super().__init__()
        main_v_layout = QVBoxLayout()
        input_h_layout = QHBoxLayout()

        self.plot_window = pg.plot()

        main_v_layout.addLayout(input_h_layout)
        main_v_layout.addWidget(self.plot_window)
        self.setLayout(main_v_layout)

        cm_text = QLabel("CM:")
        self.cm_combo_box = QComboBox()
        cav_text = QLabel("Cav:")
        self.cav_combo_box = QComboBox()

        end_date_time = QDateTime.currentDateTime()
        min_date_time = QDateTime.addSecs(end_date_time, 30 * -60)

        start_text = QLabel("Start:")
        self.start_selector = QDateTimeEdit()
        end_text = QLabel("End:")
        self.end_selector = QDateTimeEdit()

        self.start_selector.setMinimumDateTime(min_date_time)
        self.end_selector.setMinimumDateTime(end_date_time)

        self.plot_button = QPushButton()
        self.plot_button.setText("Update Bar Chart")

        input_h_layout.addWidget(cm_text)
        input_h_layout.addWidget(self.cm_combo_box)
        input_h_layout.addWidget(cav_text)
        input_h_layout.addWidget(self.cav_combo_box)
        input_h_layout.addWidget(start_text)
        input_h_layout.addWidget(self.start_selector)
        input_h_layout.addWidget(end_text)
        input_h_layout.addWidget(self.end_selector)
        input_h_layout.addWidget(self.plot_button)

        self.cm_combo_box.addItems(ALL_CRYOMODULES)
        self.cav_combo_box.addItems([str(i) for i in range(1, 9)])

        self.x_data = None
        self.y_data = None

        self.plot_button.clicked.connect(self.update_plot)

    def get_data(self):
        cavity: BackendCavity = DISPLAY_MACHINE.cryomodules[self.cm_combo_box.currentText()].cavities[
            int(self.cav_combo_box.currentText())]

        self.x_data = []
        self.y_data = []

        start = self.start_selector.dateTime().toPyDateTime()
        end = self.end_selector.dateTime().toPyDateTime()

        # Ex. result is a dictionary with key=fault pv string, value=FaultCounter(fault_count=0, ok_count=1, invalid_count=0)
        result: Dict[str, FaultCounter] = cavity.get_fault_counts(
            start, end
        )
        for tlc, counter_obj in result.items():
            self.x_data.append(tlc)  # x axis
            self.y_data.append(counter_obj.sum_fault_count)  # y axis

    def update_plot(self):
        self.get_data()

        ticks = []
        x_vals_ints = []
        for idx, x_val in enumerate(self.x_data):
            ticks.append((idx + 1, x_val))
            x_vals_ints.append(idx + 1)

        # Create pyqt5graph bar graph item with green bars
        # bargraph = pg.BarGraphItem(x=x_vals_ints, height=self.y_data, width=0.6, brush="g")
        bargraph = pg.BarGraphItem(x0=0, y=x_vals_ints, height=0.6, width=self.y_data, brush='b')

        ax = self.plot_window.getAxis("left")
        self.plot_window.setWindowTitle("title")
        ax.setTicks([ticks])
        self.plot_window.showGrid(x=True, y=False, alpha=0.6)
        self.plot_window.addItem(bargraph)
