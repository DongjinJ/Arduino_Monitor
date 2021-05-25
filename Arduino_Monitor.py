from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvas as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class ArduinoApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        canvas = FigureCanvas(Figure(figsize=(4,3)))
        gbox = QGridLayout(self.main_widget)
        gbox.addWidget(canvas, 0, 1)

        self.addToolBar(NavigationToolbar(canvas, self))

        self.ax = canvas.figure.subplots()