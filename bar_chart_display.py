import pyqtgraph as pg
from PyQt5.QtWidgets import QVBoxLayout
# from PyQt5.QtChart import QChart, QChartView, QBarSet, QPercentBarSeries, QBarCategoryAxis
from pydm import Display

from frontend.cavity_widget import GREEN_FILL_COLOR


class BarChart(Display):
    def __init__(self, parent=None, args=None):
        super().__init__(parent, args)

        self.setWindowTitle("Bar Chart")
        vertLayout_Form = QVBoxLayout()

        # Make plot window and add it to the vert layout
        self.plot_window = pg.plot()
        vertLayout_Form.addWidget(self.plot_window)

        self.setLayout(vertLayout_Form)

        # TODO Remove these hardcoded x_vals and y_data
        x_vals_faults = [2, 4, 6, 8]
        x_vals_invalid = [10, 12, 14, 16]

        y_data = ['OFF', 'PZO', 'MGT', 'AOT']

        ticks = []
        y_vals_ints = []
        for idy, y_val in enumerate(y_data):
            ticks.append((idy, y_val))
            y_vals_ints.append(idy)

        # Attempting to stack bar chart
        bargraph = pg.BarGraphItem(x0=0, y=y_vals_ints, height=0.6, width=x_vals_faults, brush=GREEN_FILL_COLOR)
        self.plot_window.addItem(bargraph)
        bargraph = pg.BarGraphItem(x0=x_vals_faults, y=y_vals_ints, height=0.6, width=x_vals_invalid, brush='b')
        self.plot_window.addItem(bargraph)

        ax = self.plot_window.getAxis('left')
        ax.setTicks([ticks])
        self.plot_window.showGrid(x=False, y=True, alpha=0.6)
