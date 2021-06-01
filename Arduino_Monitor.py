import sys
import threading
import time
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np
from numpy.core.arrayprint import DatetimeFormat
from matplotlib.backends.backend_qt5agg import FigureCanvas as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import Data_Packet as DP
from threading import Thread
import atexit

rxdataList = []
quit_flag = False

def quit_Action():
    global quit_flag
    quit_flag = True
atexit.register(quit_Action)

class ComboBox(QComboBox):
    popupAboutToBeShown = pyqtSignal()

    def showPopup(self):
        self.popupAboutToBeShown.emit()
        super(ComboBox, self).showPopup()

class ArduinoApp(QMainWindow):
    global rxdataList
    def __init__(self):
        super().__init__()

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        gbox = QGridLayout(self.main_widget)

        # Serial Port ComboBox #
        self.cb_port = QComboBox(self)
        gbox.addWidget(self.cb_port, 0, 0, 1, 3)

        # Connect Button #
        self.bt_connect = QPushButton('Connect', self)
        self.bt_connect.clicked.connect(self.connect_Function)
        gbox.addWidget(self.bt_connect, 0, 3, 1, 1)
        
        # Logging Button #
        self.bt_logging = QPushButton('Logging', self)
        self.bt_logging.clicked.connect(self.logging_Function)
        gbox.addWidget(self.bt_logging, 0, 4, 1, 1)

        # LCD 1 ComboBox #
        self.cb_lcd_1 = ComboBox(self)
        self.cb_lcd_1.activated.connect(self.load_DataList)
        gbox.addWidget(self.cb_lcd_1, 1, 0, 1, 1)

        # LCD Widget 1 #
        self.lcd_1 = QLCDNumber(self)
        self.lcd_1.display('')
        self.lcd_1.setDigitCount(8)
        gbox.addWidget(self.lcd_1, 1, 1, 1, 3)

        # LCD 2 ComboBox #
        self.cb_lcd_2 = QComboBox(self)
        self.cb_lcd_2.activated.connect(self.load_DataList)
        gbox.addWidget(self.cb_lcd_2, 2, 0, 1, 1)
        
        # LCD Widget 2 #
        self.lcd_2 = QLCDNumber(self)
        self.lcd_2.display('0')
        self.lcd_2.setDigitCount(8)
        gbox.addWidget(self.lcd_2, 2, 1, 1, 3)

        # LCD 3 ComboBox #
        self.cb_lcd_3 = QComboBox(self)
        self.cb_lcd_3.activated.connect(self.load_DataList)
        gbox.addWidget(self.cb_lcd_3, 3, 0, 1, 1)
        
        # LCD Widget 3 #
        self.lcd_3 = QLCDNumber(self)
        self.lcd_3.display('0.0')
        self.lcd_3.setDigitCount(8)
        gbox.addWidget(self.lcd_3, 3, 1, 1, 3)

        # Data Plot Label #
        self.lb_data_plot = QLabel('Plot Data', self)
        gbox.addWidget(self.lb_data_plot, 0, 6)

        # Data Plot ComboBox #
        self.cb_data_plot = QComboBox(self)
        self.cb_data_plot.highlighted.connect(self.load_DataList)
        gbox.addWidget(self.cb_data_plot, 0, 7)

        # Data Plot #
        canvas = FigureCanvas(Figure(figsize=(4,4)))
        gbox.addWidget(canvas, 1, 4, 4, 4)

        self.data_plot = canvas.figure.subplots()
        self.x_data = []
        self.y_data = []
        self.data_plot.plot(self.x_data, self.y_data, '-')

        # x ms Timer (x는 조정 필요) #
        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)

        self.setWindowTitle('Arduino Monitor')
        self.setGeometry(300, 100, 600, 400)
        self.show()
    def load_DataList(self):
        global rxdataList
        print("Load")
        for i in range(len(rxdataList)):
            self.cb_data_plot.additem(rxdataList[i].get_ID())
            self.cb_lcd_1.additem(rxdataList[i].get_ID())
            self.cb_lcd_2.additem(rxdataList[i].get_ID())
            self.cb_lcd_3.additem(rxdataList[i].get_ID())

    def connect_Function(self):
        # Serial Connect Part #
        pass

    def logging_Function(self):
        self.timer.start()

    def update_plot(self):
        self.data_plot.clear()
        t = time.time()
        self.x_data.append(t)
        self.y_data.append(np.sin(t))
        self.data_plot.plot(self.x_data, self.y_data, '-', color='deeppink')
        self.data_plot.figure.canvas.draw()
        sender = self.sender()
        currentTime = QTime.currentTime().toString("hh:mm:ss")
        if id(sender) == id(self.timer):
            self.lcd_1.display(currentTime)

    def closeEvent(self, a0: QCloseEvent) -> None:
        global quit_flag
        quit_flag = True
        return super().closeEvent(a0)

def debug_Input():
    global rxdataList
    while not quit_flag:
        rw = input("RW: ")
        id = input("ID: ")
        data = input("DATA: ")

        if not rxdataList:
            rxdataList.append(DP.arduinoData())
            rxdataList[-1].update_ID(id)
            rxdataList[-1].update_Data(data)
        else:
            update = False
            for i in range(len(rxdataList)):
                if rxdataList[i].get_ID() == id:
                    rxdataList[i].update_Data(data)
                    update = True
                else:
                    pass
            if update == False:
                rxdataList.append(DP.arduinoData())
                rxdataList[-1].update_ID(id)
                rxdataList[-1].update_Data(data)
        for i in range(len(rxdataList)):
            print(rxdataList[i].get_ID(), ": ", rxdataList[i].get_Data())

if __name__ == '__main__':
    task1 = Thread(target=debug_Input, args=())
    task1.start()
    app = QApplication(sys.argv)
    ex = ArduinoApp()
    sys.exit(app.exec_())