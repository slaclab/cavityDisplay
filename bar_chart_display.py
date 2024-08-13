import pyqtgraph as pg
from PyQt5.QtWidgets import QVBoxLayout
# from PyQt5.QtChart import QChart, QChartView, QBarSet, QPercentBarSeries, QBarCategoryAxis
from pydm import Display


class BarChart(Display):
    def __init__(self, parent=None, args=None):
        super().__init__(parent, args)

        self.setWindowTitle("Bar Chart")
        vertLayout_Form = QVBoxLayout()

        # Make plot window and add it to the vert layout
        self.plot_window = pg.plot()
        vertLayout_Form.addWidget(self.plot_window)

        self.setLayout(vertLayout_Form)

        # TODO Remove these hardcoded x_vals and y_vals
        x_vals = ['OFF', 'PZO', 'MGT', 'AOT']
        y_vals_faults = [1, 6, 2, 1]
        y_vals_invalid = [10, 11, 12, 1]
        x_vals_ints = []

        ticks = []
        for idx, x_val in enumerate(x_vals):
            ticks.append((idx, x_val))
            x_vals_ints.append(idx)

        # Attempting to stack bar chart
        bottom = [0, 0, 0, 0]
        bargraph = pg.BarGraphItem(x=x_vals_ints, height=y_vals_faults, width=0.6, brush='g')
        self.plot_window.addItem(bargraph)
        bargraph = pg.BarGraphItem(x=x_vals_ints, height=y_vals_invalid, y0=y_vals_faults, width=0.6, brush='b')
        self.plot_window.addItem(bargraph)

        '''
        # Create pyqt5graph bar graph item with green bars
        bargraph = pg.BarGraphItem(x=x_vals_ints, height=y_vals_faults, width=0.6, brush='g')
        # bargraph = pg.BarGraphItem(x0=0, y=x_vals_ints, height=0.6, width=y_vals, brush='b')

        # ax = self.plot_window.getAxis('left')
        ax = self.plot_window.getAxis('bottom')
        ax.setTicks([ticks])
        self.plot_window.showGrid(x=False, y=True, alpha=0.6)

        # Add bargraph to plot window
        self.plot_window.addItem(bargraph)
        '''
