import sys
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
import serial
import serial.tools.list_ports as sp

rxdataList = []
dataTable = [-1, -1, -1, -1, -1]
quit_flag = False
connect_flag = False
ser = None

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
        self.serialTask = None

        self.pen = QPen(QColor(0, 0, 0, 255))
        self.pen.setWidth(2)
        self.gauge_data = 0
        self.gauge_data_prev = 0

        self.scale_polygon_colors = []
        self.set_scale_polygon_colors([[.00, Qt.red],
                                     [.4, Qt.yellow],
                                     [.8, Qt.green],
                                     [1., Qt.transparent]])

        # Serial Port ComboBox #
        self.cb_port = ComboBox(self)
        self.cb_port.addItem("Port")
        self.cb_port.popupAboutToBeShown.connect(self.load_serialPort)
        self.cb_port.setGeometry(15, 10, 100, 25)


        # Connect Button #
        self.bt_connect = QPushButton('Connect', self)
        self.bt_connect.clicked.connect(self.connect_Function)
        self.bt_connect.setGeometry(125, 10, 90, 25)

        
        # Logging Button #
        self.bt_logging = QPushButton('Logging', self)
        self.bt_logging.clicked.connect(self.logging_Function)
        self.bt_logging.setGeometry(225, 10, 90, 25)


        # Connect State Label #
        self.lb_connect_state = QLabel('Disconnect', self)
        self.lb_connect_state.setAlignment(Qt.AlignLeft)
        self.font_lb = self.lb_connect_state.font()
        self.font_lb.setPointSize(9)
        #self.font_lb.setFamily('Times New Roman')
        self.font_lb.setBold(True)
        self.lb_connect_state.setFont(self.font_lb)
        self.lb_connect_state.setStyleSheet("color: red")
        self.lb_connect_state.setGeometry(330, 15, 90, 25)

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

        # Gauge ComboBox #
        self.cb_gauge = ComboBox(self)
        self.cb_gauge.addItem("Gauge")
        self.cb_gauge.activated[str].connect(self.select_data_gauge)
        self.cb_gauge.popupAboutToBeShown.connect(self.load_DataList_gauge)
        self.cb_gauge.setGeometry(15, 240, 100, 25)

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
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_Data)

        self.setWindowTitle('Arduino Monitor')
        self.setFixedSize(740, 460)
        self.show()

    def paintEvent(self, event):
        self.draw_Gauge(165, 370)
        self.draw_scaled_marker(165, 370)
        if self.gauge_data != self.gauge_data_prev:
            if self.gauge_data_prev > self.gauge_data:
                self.gauge_data_prev -= 1
            elif self.gauge_data_prev < self.gauge_data:
                self.gauge_data_prev += 1
        self.draw_Needle(165, 370, self.gauge_data_prev)

    def draw_Needle(self, x_center, y_center, value):
        my_painter = QPainter(self)
        my_painter.setRenderHint(QPainter.Antialiasing)
        self.pen = QPen(QColor(50, 50, 50, 255))
        self.pen.setWidth(2)
        my_painter.setPen(self.pen)
        if value > 180:
            value = 180
        theta = (270 / 180) * value + 135
        x = x_center + math.cos(math.radians(theta)) * 60
        y = y_center + math.sin(math.radians(theta)) * 60
        my_painter.drawLine(x_center, y_center, round(x), round(y))
        my_painter.end()

    def draw_Gauge(self, x_center, y_center):
        self.painter_filled_polygon = QPainter(self)
        self.painter_filled_polygon.setRenderHint(QPainter.Antialiasing)
        self.painter_filled_polygon.setPen(Qt.NoPen)
        self.painter_filled_polygon.setBrush(QColor(50, 50, 50, 255))
        self.painter_filled_polygon.drawEllipse(round(x_center - 7.5), round(y_center - 7.5), 15, 15)

        self.polygon = QPolygonF()
        length = 100
        for theta in range(135, 405):
            x = x_center + math.cos(math.radians(theta)) * length
            y = y_center + math.sin(math.radians(theta)) * length
            self.polygon.append(QPointF(x, y))
        length = 105
        for theta in range(135, 405):
            x = x_center + math.cos(math.radians(theta)) * length
            y = y_center + math.sin(math.radians(theta)) * length
            self.polygon.append(QPointF(x, y))
        self.polygon.append(QPointF(x, y))
        self.grad = QConicalGradient(QPointF(x_center,y_center), -45)
        for eachcolor in self.scale_polygon_colors:
            self.grad.setColorAt(eachcolor[0], eachcolor[1])
        self.painter_filled_polygon.setPen(Qt.NoPen)
        self.painter_filled_polygon.setBrush(self.grad)
        #self.painter_filled_polygon.setPen(QPen(Qt.black, 2))
        self.painter_filled_polygon.drawPolygon(self.polygon)
        self.painter_filled_polygon.end()

    def draw_scaled_marker(self, x_center, y_center):
        my_painter = QPainter(self)
        my_painter.setRenderHint(QPainter.Antialiasing)
        self.pen = QPen(QColor(0,0,0,255))
        self.pen.setWidth(2)
        my_painter.setPen(self.pen)
        font = QFont("Decorative", 15)
        fm = QFontMetrics(font)

        for theta in range(135, 415, 15):
            i = (theta - 135) / 15 * 10
            text = str(int(i))
            w = fm.width(text) + 1
            h = fm.height()
            x_1 = x_center + math.cos(math.radians(theta)) * 95
            y_1 = y_center + math.sin(math.radians(theta)) * 95
            x_2 = x_center + math.cos(math.radians(theta)) * 104
            y_2 = y_center + math.sin(math.radians(theta)) * 104
            x = x_center + math.cos(math.radians(theta)) * 80
            y = y_center + math.sin(math.radians(theta)) * 80
            my_painter.drawText(round(x - w/2), round(y - h/2), round(w), round(h), Qt.AlignCenter, text)
            my_painter.drawLine(round(x_1), round(y_1), round(x_2), round(y_2))
        for theta in range(135, 405, 3):
            x_1 = x_center + math.cos(math.radians(theta)) * 99
            y_1 = y_center + math.sin(math.radians(theta)) * 99
            x_2 = x_center + math.cos(math.radians(theta)) * 104
            y_2 = y_center + math.sin(math.radians(theta)) * 104
            my_painter.drawLine(round(x_1), round(y_1), round(x_2), round(y_2))

        my_painter.end()

    def set_scale_polygon_colors(self, color_array):
        # print(type(color_array))
        if 'list' in str(type(color_array)):
            self.scale_polygon_colors = color_array
        elif color_array == None:
            self.scale_polygon_colors = [[.0, Qt.transparent]]
        else:
            self.scale_polygon_colors = [[.0, Qt.transparent]]
    
    def select_data_plot(self, cur_ID):
        if cur_ID != '':
            for i in range(len(rxdataList)):
                if str(rxdataList[i].get_ID()) == cur_ID:
                    dataTable[0] = i
                    break
        else:
            dataTable[0] = -1

    def select_data_lcd1(self, cur_ID):
        if cur_ID != '':
            for i in range(len(rxdataList)):
                if str(rxdataList[i].get_ID()) == cur_ID:
                    dataTable[1] = i
                    break
        else:
            dataTable[1] = -1

    def select_data_lcd2(self, cur_ID):
        if cur_ID != '':
            for i in range(len(rxdataList)):
                if str(rxdataList[i].get_ID()) == cur_ID:
                    dataTable[2] = i
                    break
        else:
            dataTable[2] = -1

    def select_data_lcd3(self, cur_ID):
        if cur_ID != '':
            for i in range(len(rxdataList)):
                if str(rxdataList[i].get_ID()) == cur_ID:
                    dataTable[3] = i
                    break
        else:
            dataTable[3] = -1
    
    def select_data_gauge(self, cur_ID):
        if cur_ID != '':
            for i in range(len(rxdataList)):
                if str(rxdataList[i].get_ID()) == cur_ID:
                    dataTable[4] = i
                    break
        else:
            dataTable[4] = -1

    def load_DataList_plot(self):
        global rxdataList
        self.cb_data_plot.clear()
        self.cb_data_plot.addItem('')
        for i in range(len(rxdataList)):
            self.cb_data_plot.addItem(str(rxdataList[i].get_ID()))

    def load_DataList_lcd1(self):
        global rxdataList
        self.cb_lcd_1.clear()
        self.cb_lcd_1.addItem('')
        for i in range(len(rxdataList)):
            self.cb_lcd_1.addItem(str(rxdataList[i].get_ID()))

    def load_DataList_lcd2(self):
        global rxdataList
        self.cb_lcd_2.clear()
        self.cb_lcd_2.addItem('')
        for i in range(len(rxdataList)):
            self.cb_lcd_2.addItem(str(rxdataList[i].get_ID()))

    def load_DataList_lcd3(self):
        global rxdataList
        self.cb_lcd_3.clear()
        self.cb_lcd_3.addItem('')
        for i in range(len(rxdataList)):
            self.cb_lcd_3.addItem(str(rxdataList[i].get_ID()))

    def load_DataList_gauge(self):
        global rxdataList
        self.cb_gauge.clear()
        self.cb_gauge.addItem('')
        for i in range(len(rxdataList)):
            self.cb_gauge.addItem(str(rxdataList[i].get_ID()))

    def connect_Function(self):
        # Serial Connect Part #
        global ser
        global connect_flag
        if ser != None:
            if ser.is_open:
                ser.close()
                connect_flag = False
                self.serialTask.join()
        ser = serial.Serial(str(self.cb_port.currentText()), 115200, timeout=1)
        connect_flag = True
        self.lb_connect_state.setText("Connect")
        self.lb_connect_state.setStyleSheet("color: green")
        self.serialTask = Thread(target=serial_Input)
        self.serialTask.start()
        self.timer.start()
    
    def load_serialPort(self):
        # Load Serial Port #
        self.uartList = []
        list = sp.comports()

        for i in list:
            self.uartList.append(i.device)
        self.cb_port.clear()
        self.cb_port.addItems(self.uartList)

    def logging_Function(self):
        pass

    def update_Data(self):
        self.update()
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
            self.lcd_2.display(str(rxdataList[dataTable[2]].get_Data()))
        if dataTable[3] != -1:
            self.lcd_3.display(str(rxdataList[dataTable[3]].get_Data()))
        if dataTable[4] != -1:
            self.gauge_data = rxdataList[dataTable[4]].get_Data()


    def closeEvent(self, a0: QCloseEvent) -> None:
        global quit_flag
        global connect_flag
        global ser
        if ser != None:
            ser.close()
        connect_flag = False
        self.serialTask.join()
        quit_flag = True
        return super().closeEvent(a0)

def serial_Input():
    while connect_flag:
        rx_buf = []
        if ser.in_waiting:
            for i in range(4):
                rx_buf.append(ser.read())
            id_temp, data_temp = DP.decode_Data(rx_buf)
            print("id: ", type(id_temp), "/ Data: ", type(data_temp))
            if id_temp != None or data_temp != None:
                if not rxdataList:
                    rxdataList.append(DP.arduinoData())
                    rxdataList[-1].update_ID(id_temp)
                    rxdataList[-1].update_Data(data_temp)
                else:
                    update = False
                    for i in range(len(rxdataList)):
                        if rxdataList[i].get_ID() == id_temp:
                            rxdataList[i].update_Data(data_temp)
                            update = True
                        else:
                            pass
                    if update == False:
                        rxdataList.append(DP.arduinoData())
                        rxdataList[-1].update_ID(id_temp)
                        rxdataList[-1].update_Data(data_temp)


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
    #task1 = Thread(target=debug_Input, args=())
    #task1.start()
    app = QApplication(sys.argv)
    ex = ArduinoApp()
    sys.exit(app.exec_())   