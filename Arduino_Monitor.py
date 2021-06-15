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
import math

rxdataList = []
dataTable = [-1, -1, -1, -1]
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

        self.pen = QPen(QColor(0, 0, 0, 255))
        self.pen.setWidth(2)
        self.set_scale_polygon_colors = ([[.00, Qt.red],
                                     [.1, Qt.yellow],
                                     [.15, Qt.green],
                                     [1, Qt.transparent]])

        # Serial Port ComboBox #
        self.cb_port = ComboBox(self)
        self.cb_port.addItem("Port")
        self.cb_port.setGeometry(15, 10, 100, 25)


        # Connect Button #
        self.bt_connect = QPushButton('Connect', self)
        self.bt_connect.clicked.connect(self.connect_Function)
        self.bt_connect.setGeometry(125, 10, 90, 25)

        
        # Logging Button #
        self.bt_logging = QPushButton('Logging', self)
        self.bt_logging.clicked.connect(self.logging_Function)
        self.bt_logging.setGeometry(225, 10, 90, 25)


        # LCD 1 ComboBox #
        self.cb_lcd_1 = ComboBox(self)
        self.cb_lcd_1.addItem("LCD 1")
        self.cb_lcd_1.activated[str].connect(self.select_data_lcd1)
        self.cb_lcd_1.popupAboutToBeShown.connect(self.load_DataList_lcd1)
        self.cb_lcd_1.setGeometry(15, 50, 100, 25)


        # LCD Widget 1 #
        self.lcd_1 = QLCDNumber(self)
        self.lcd_1.display('')
        self.lcd_1.setDigitCount(8)
        self.lcd_1.setGeometry(125, 50, 190, 60)


        # LCD 2 ComboBox #
        self.cb_lcd_2 = ComboBox(self)
        self.cb_lcd_2.addItem("LCD 2")
        self.cb_lcd_2.activated[str].connect(self.select_data_lcd2)
        self.cb_lcd_2.popupAboutToBeShown.connect(self.load_DataList_lcd2)
        self.cb_lcd_2.setGeometry(15, 120, 100, 25)

        
        # LCD Widget 2 #
        self.lcd_2 = QLCDNumber(self)
        self.lcd_2.display('0')
        self.lcd_2.setDigitCount(8)
        self.lcd_2.setGeometry(125, 120, 190, 60)


        # LCD 3 ComboBox #
        self.cb_lcd_3 = ComboBox(self)
        self.cb_lcd_3.addItem("LCD 3")
        self.cb_lcd_3.activated[str].connect(self.select_data_lcd3)
        self.cb_lcd_3.popupAboutToBeShown.connect(self.load_DataList_lcd3)
        self.cb_lcd_3.setGeometry(15, 190, 100, 25)

        
        # LCD Widget 3 #
        self.lcd_3 = QLCDNumber(self)
        self.lcd_3.display('0.0')
        self.lcd_3.setDigitCount(8)
        self.lcd_3.setGeometry(125, 190, 190, 60)


        # Data Plot Label #
        self.lb_data_plot = QLabel('Plot Data: ', self)
        self.lb_data_plot.setGeometry(490, 13, 90, 25)
   

        # Data Plot ComboBox #
        self.cb_data_plot = ComboBox(self)
        self.cb_data_plot.addItem("Data Plot")
        self.cb_data_plot.activated[str].connect(self.select_data_plot)
        self.cb_data_plot.popupAboutToBeShown.connect(self.load_DataList_plot)
        self.cb_data_plot.setGeometry(550, 10, 100, 25)


        # Data Plot #
        self.canvas = FigureCanvas(Figure(figsize=(4,4)))
        self.canvas.setParent(self)
        self.canvas.move(330, 50)
        #gbox.addWidget(canvas, 1, 4, 4, 4)

        self.data_plot = self.canvas.figure.subplots()
        self.x_data = []
        self.y_data = []
        self.data_plot.plot(self.x_data, self.y_data, '-')

        # x ms Timer (x는 조정 필요) #
        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_Data)

        self.setWindowTitle('Arduino Monitor')
        self.setFixedSize(740, 460)
        self.show()

    def paintEvent(self, event):
        self.draw_Gauge(165, 370)
        

    def draw_Gauge(self, x_center, y_center):
        self.painter_filled_polygon = QPainter(self)
        self.painter_filled_polygon.setRenderHint(QPainter.Antialiasing)
        self.painter_filled_polygon.translate(self.width() / 2, self.height() / 2)
        self.painter_filled_polygon.setPen(Qt.NoPen)
        self.painter_filled_polygon.drawPoint(x_center, y_center)

        self.polygon = QPolygonF()
        length = 100
        for theta in range(135, 405):
            x = x_center + math.cos(math.radians(theta)) * length
            y = y_center + math.sin(math.radians(theta)) * length
            self.polygon.append(QPoint(x, y))
        length = 105
        for theta in range(135, 405):
            x = x_center + math.cos(math.radians(theta)) * length
            y = y_center + math.sin(math.radians(theta)) * length
            self.polygon.append(QPoint(x, y))
        #self.grad = 
        self.painter_filled_polygon.setPen(QPen(Qt.black, 2))
        self.painter_filled_polygon.drawPolygon(self.polygon)
        self.painter_filled_polygon.end()


    def select_data_plot(self, cur_ID):
        if cur_ID != '':
            for i in range(len(rxdataList)):
                if rxdataList[i].get_ID() == cur_ID:
                    dataTable[0] = i
                    break
        else:
            dataTable[0] = -1

    def select_data_lcd1(self, cur_ID):
        if cur_ID != '':
            for i in range(len(rxdataList)):
                if rxdataList[i].get_ID() == cur_ID:
                    dataTable[1] = i
                    break
        else:
            dataTable[1] = -1

    def select_data_lcd2(self, cur_ID):
        if cur_ID != '':
            for i in range(len(rxdataList)):
                if rxdataList[i].get_ID() == cur_ID:
                    dataTable[2] = i
                    break
        else:
            dataTable[2] = -1

    def select_data_lcd3(self, cur_ID):
        if cur_ID != '':
            for i in range(len(rxdataList)):
                if rxdataList[i].get_ID() == cur_ID:
                    dataTable[3] = i
                    break
        else:
            dataTable[3] = -1

    def load_DataList_plot(self):
        global rxdataList
        self.cb_data_plot.clear()
        self.cb_data_plot.addItem('')
        for i in range(len(rxdataList)):
            self.cb_data_plot.addItem(rxdataList[i].get_ID())

    def load_DataList_lcd1(self):
        global rxdataList
        self.cb_lcd_1.clear()
        self.cb_lcd_1.addItem('')
        for i in range(len(rxdataList)):
            self.cb_lcd_1.addItem(rxdataList[i].get_ID())

    def load_DataList_lcd2(self):
        global rxdataList
        self.cb_lcd_2.clear()
        self.cb_lcd_2.addItem('')
        for i in range(len(rxdataList)):
            self.cb_lcd_2.addItem(rxdataList[i].get_ID())

    def load_DataList_lcd3(self):
        global rxdataList
        self.cb_lcd_3.clear()
        self.cb_lcd_3.addItem('')
        for i in range(len(rxdataList)):
            self.cb_lcd_3.addItem(rxdataList[i].get_ID())

    def connect_Function(self):
        # Serial Connect Part #
        pass

    def logging_Function(self):
        self.timer.start()

    def update_Data(self):
        if dataTable[0] != -1:
            self.data_plot.clear()
            t = time.time()
            self.x_data.append(t)
            self.y_data.append(rxdataList[dataTable[0]].get_Data())
            self.data_plot.plot(self.x_data, self.y_data, '-', color='deeppink')
            self.data_plot.figure.canvas.draw()
        if dataTable[1] != -1:
            self.lcd_1.display(str(rxdataList[dataTable[1]].get_Data()))
        if dataTable[2] != -1:
            self.lcd_1.display(str(rxdataList[dataTable[2]].get_Data()))
        if dataTable[3] != -1:
            self.lcd_1.display(str(rxdataList[dataTable[3]].get_Data()))


    def closeEvent(self, a0: QCloseEvent) -> None:
        global quit_flag
        quit_flag = True
        return super().closeEvent(a0)

def debug_Input():
    global rxdataList
    while not quit_flag:
        id = input("ID: ")
        data = input("DATA: ")

        if not rxdataList:
            rxdataList.append(DP.arduinoData())
            rxdataList[-1].update_ID(id)
            rxdataList[-1].update_Data(int(data))
        else:
            update = False
            for i in range(len(rxdataList)):
                if rxdataList[i].get_ID() == id:
                    rxdataList[i].update_Data(int(data))
                    update = True
                else:
                    pass
            if update == False:
                rxdataList.append(DP.arduinoData())
                rxdataList[-1].update_ID(id)
                rxdataList[-1].update_Data(int(data))
        for i in range(len(rxdataList)):
            print("[", rxdataList[i].get_ID(), "]: ", rxdataList[i].get_Data())

if __name__ == '__main__':
    task1 = Thread(target=debug_Input, args=())
    task1.start()
    app = QApplication(sys.argv)
    ex = ArduinoApp()
    sys.exit(app.exec_())