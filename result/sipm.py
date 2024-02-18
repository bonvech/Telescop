import sys
import pandas as pd
import os
import colorsys
from PyQt6 import uic  # Импортируем uic
from PyQt6.QtWidgets import QApplication, QDialog, QFileDialog, QMainWindow, QVBoxLayout, QLabel
from PyQt6.QtGui import QPixmap, QFont
from PyQt6 import QtCore, QtGui, QtWidgets

from matplotlib.colors import Normalize
import numpy as np
import matplotlib.cm as cm
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt


def drow(d, q, theme):
        global File
        global Event
        sipm = []
        ch = []
        znach = []
        X = []
        Y = []

        o = File[File['Event'] == int(Event)]

        for i in q[q['SIPM'] == 1]['ch'].unique().tolist():
            sipm.append(1)
            ch.append(i)
            znach.append(max(o[(o['SIPM'] == 1) & (o['ch'] == i)].iloc[0, 229:230]))
        #print(o[(o['SIPM'] == 1) & (o['ch'] == i)].iloc[0, 4:1024])

        for i in q[q['SIPM'] == 2]['ch'].unique().tolist():
            sipm.append(2)
            ch.append(i)
            znach.append(max(o[(o['SIPM'] == 2) & (o['ch'] == i)].iloc[0, 100:1000]))

        cmap = cm.get_cmap(theme)

        norm = Normalize(vmin=min(znach), vmax=max(znach))
        rgba_values = cmap(norm(znach))

        for Si, c, col, z in zip(sipm, ch, rgba_values, znach):
            for i in d:   
                if i.sipm == Si and i.pin == c:
                    i.rgbcol = col
                    print(col)
                    h, l, s = colorsys.rgb_to_hls(col[0], col[1], col[2])
                    print(h)
                    h = (h + 0.7) % 1
                    s = (s + 0.7) % 1
                    l = (l + 0.7) % 1
                    print(s, l)
                    print(colorsys.hls_to_rgb(h, l, s))
                    i.textcol = matplotlib.colors.rgb2hex(colorsys.hls_to_rgb(h, s, l))
                    print(i.textcol)
                    i.col = matplotlib.colors.rgb2hex(col)
                    i.setStyleSheet("QPushButton {background-color: "+ i.col +" ; color: White;  border-radius: "+str(int(i.frameSize().width()/2))+"px; }"
                                        "QPushButton:pressed {background-color:#b784a7)} ;")         
                    print(str(col))
                    i.znach = z
                    i.setText(f'{z}\nSIPM:{i.sipm}\nPin:{i.pin}')
                    print(z)
                    print(i.znach)

                    break
        ex.b()
                    

File = pd.DataFrame()
Event = ''

def Data(filename):
    global File
    columns = ['Event', 'SIPM', 'SIPMKadr', 'Time', 'ch'] + [f'{i}' for i in range(1024)]
    df = pd.read_csv(filename, sep="\s+", encoding="windows-1251", header=None, index_col=False, names=columns)
    df = df.dropna()
    df['SIPM'] = df["SIPM"].astype(int)
    df['ch'] = df["ch"].astype(int)
    File = df



class MyWidget(QMainWindow):
    resized = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        uic.loadUi('sc.ui', self)
        self.setMinimumWidth(650)
        self.setMinimumHeight(450)
        self.Open.triggered.connect(self.OpenF)
        self.resized.connect(self.b) # Загружаем дизайн
        self.d = []
        self.d.append(self.S1P0)
        self.S1P0.sipm = 1
        self.S1P0.pin = 0
        self.d.append(self.S1P1)
        self.S1P1.sipm = 1
        self.S1P1.pin = 1
        self.d.append(self.S1P2)
        self.S1P2.sipm = 1
        self.S1P2.pin = 2
        self.d.append(self.S1P3)
        self.S1P3.sipm = 1
        self.S1P3.pin = 3
        self.d.append(self.S1P4)
        self.S1P4.sipm = 1
        self.S1P4.pin = 4
        self.d.append(self.S1P5)
        self.S1P5.sipm = 1
        self.S1P5.pin = 5
        self.d.append(self.S1P6)
        self.S1P6.sipm = 1
        self.S1P6.pin = 6
        self.d.append(self.S1P16)
        self.S1P16.sipm = 1
        self.S1P16.pin = 16
        self.d.append(self.S1P17)
        self.S1P17.sipm = 1
        self.S1P17.pin = 17
        self.d.append(self.S1P18)
        self.S1P18.sipm = 1
        self.S1P18.pin = 18
        self.d.append(self.S1P19)
        self.S1P19.sipm = 1
        self.S1P19.pin = 19
        self.d.append(self.S1P20)
        self.S1P20.sipm = 1
        self.S1P20.pin = 20
        self.d.append(self.S1P21)
        self.S1P21.sipm = 1
        self.S1P21.pin = 21
        self.d.append(self.S1P22)
        self.S1P22.sipm = 1
        self.S1P22.pin = 22
        self.d.append(self.S1P24)
        self.S1P24.sipm = 1
        self.S1P24.pin = 24
        self.d.append(self.S1P25)
        self.S1P25.sipm = 1
        self.S1P25.pin = 25
        self.d.append(self.S1P26)
        self.S1P26.sipm = 1
        self.S1P26.pin = 26
        self.d.append(self.S1P27)
        self.S1P27.sipm = 1
        self.S1P27.pin = 27
        self.d.append(self.S1P28)
        self.S1P28.sipm = 1
        self.S1P28.pin = 28
        self.d.append(self.S1P29)
        self.S1P29.sipm = 1
        self.S1P29.pin = 29
        self.d.append(self.S1P30)
        self.S1P30.sipm = 1
        self.S1P30.pin = 30
        self.d.append(self.S1P8)
        self.S1P8.sipm = 1
        self.S1P8.pin = 8
        self.d.append(self.S1P9)
        self.S1P9.sipm = 1
        self.S1P9.pin = 9
        self.d.append(self.S1P10)
        self.S1P10.sipm = 1
        self.S1P10.pin = 10
        self.d.append(self.S1P11)
        self.S1P11.sipm = 1
        self.S1P11.pin = 11
        self.d.append(self.S1P12)
        self.S1P12.sipm = 1
        self.S1P12.pin = 12
        self.d.append(self.S1P13)
        self.S1P13.sipm = 1
        self.S1P13.pin = 13
        self.d.append(self.S1P14)
        self.S1P14.sipm = 1
        self.S1P14.pin = 14
        self.d.append(self.S2P8)
        self.S2P8.sipm = 2
        self.S2P8.pin = 8
        self.d.append(self.S2P9)
        self.S2P9.sipm = 2
        self.S2P9.pin = 9
        self.d.append(self.S2P10)
        self.S2P10.sipm = 2
        self.S2P10.pin = 10
        self.d.append(self.S2P11)
        self.S2P11.sipm = 2
        self.S2P11.pin = 11
        self.d.append(self.S2P12)
        self.S2P12.sipm = 2
        self.S2P12.pin = 12
        self.d.append(self.S2P13)
        self.S2P13.sipm = 2
        self.S2P13.pin = 13
        self.d.append(self.S2P14)
        self.S2P14.sipm = 2
        self.S2P14.pin = 14
        self.d.append(self.S2P0)
        self.S2P0.sipm = 2
        self.S2P0.pin = 0
        self.d.append(self.S2P1)
        self.S2P1.sipm = 2
        self.S2P1.pin = 1
        self.d.append(self.S2P2)
        self.S2P2.sipm = 2
        self.S2P2.pin = 2
        self.d.append(self.S2P3)
        self.S2P3.sipm = 2
        self.S2P3.pin = 3
        self.d.append(self.S2P4)
        self.S2P4.sipm = 2
        self.S2P4.pin = 4
        self.d.append(self.S2P5)
        self.S2P5.sipm = 2
        self.S2P5.pin = 5
        self.d.append(self.S2P6)
        self.S2P6.sipm = 2
        self.S2P6.pin = 6
        self.d.append(self.S2P16)
        self.S2P16.sipm = 2
        self.S2P16.pin = 16
        self.d.append(self.S2P17)
        self.S2P17.sipm = 2
        self.S2P17.pin = 17
        self.d.append(self.S2P18)
        self.S2P18.sipm = 2
        self.S2P18.pin = 18
        self.d.append(self.S2P19)
        self.S2P19.sipm = 2
        self.S2P19.pin = 19
        self.d.append(self.S2P20)
        self.S2P20.sipm = 2
        self.S2P20.pin = 20
        self.d.append(self.S2P21)
        self.S2P21.sipm = 2
        self.S2P21.pin = 21
        self.d.append(self.S2P22)
        self.S2P22.sipm = 2
        self.S2P22.pin = 22
        df = pd.read_csv('dat.dat', sep='\s+')
        self.df = df
        self.Events.activated.connect(self.Drow)
        self.theme.activated.connect(self.changetheme)
        self.theme.addItems(['magma', 'Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Grays', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'crest', 'crest_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'flare', 'flare_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_grey', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gist_yerg', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'grey', 'hot', 'hot_r', 'hsv', 'hsv_r', 'icefire', 'icefire_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'mako', 'mako_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'rocket', 'rocket_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'vlag', 'vlag_r', 'winter', 'winter_r'])
        for i in self.d:
            i.clicked.connect(self.on_key_click)
            i.x = self.df[((self.df['SIPM'] == i.sipm) & (self.df['ch'] == i.pin))]['x_sm'].tolist()[0]
            i.y = -self.df[((self.df['SIPM'] == i.sipm) & (self.df['ch'] == i.pin))]['y_sm'].tolist()[0]
            i.znach = None
            i.win = []
            i.textcol = 'White'
            if i.sipm == 2:
                i.col = '#1f75fe'
            else:
                i.col = '#c35831'

    def changetheme(self):
        global Event
        if Event == "":
            return None
        self.Drow()

    def on_key_click(self):
        global Event
        if Event != "":
            b = self.sender()
            b.win.append(Chan(b))
            b.win[-1].show()

    def resizeEvent(self, event):
        self.resized.emit()
        return super(MyWidget, self).resizeEvent(event)

    def OpenF(self):
        global File
        global Event
        fname = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        
        if fname[0] != '':
            Data(fname[0])
        else:
            return None
        

        self.Events.clear()
        self.Events.addItems([str(i) for i in File['Event'].unique()])
        
        Event = self.Events.currentText()

        self.FileName.setText(f"File Name {fname[0]}")
        self.Event.setText(f"Event {Event}")

        drow(self.d, self.df, self.theme.currentText())

    def Drow(self):
        global Event
        Event = self.Events.currentText()
        self.Event.setText(f"Event {Event}")
        drow(self.d, self.df, self.theme.currentText())

    def b(self):
        self.theme.move(self.centralwidget.frameSize().width() - 80, 10)
        self.Event.move(10, self.centralwidget.frameSize().height() - 40)
        self.FileName.move(10, self.centralwidget.frameSize().height() - 20)
        S = min(round(self.centralwidget.frameSize().height()/9.5), round(self.centralwidget.frameSize().width()/9.5))
        w = round(self.centralwidget.frameSize().width())/2
        h = round((self.centralwidget.frameSize().height())/2)
        for i in self.d:
            i.setFixedSize(S, S)
            
            i.setStyleSheet(" QPushButton {background-color: " + i.col + " ; color: " + i.textcol +" ; border-radius: "+str(int(i.frameSize().width()/2))+"px; font-size: " +str(int(i.frameSize().width()/4.3))+ "px ;} " # QPushButton:hover { background-color: rgb(16, 16, 24) ; color: rgb(76, 76, 76);}
                                        "QPushButton:pressed {background-color: #b784a7 ; }")            
            x = i.x
            y = i.y
            i.move(round(x * S / 2.8 + w), round(y * S / 2.9 + h) - 40)

class Chan(QMainWindow):
    def __init__(self, b):
        global Event
        global File
        
        super().__init__()
        uic.loadUi('pi.ui', self)
        self.setWindowTitle(f"Chan {b.pin} SIPM {b.sipm}")
        self.setFixedSize(700, 800)
        self.chan.setText(f"Chan: {b.pin}")
        self.SIPM.setText(f"SIPM: {b.sipm}")
        self.nowevent.setText(f"Now Event: {Event}")
        self.events.clear()
        self.events.addItems([str(i) for i in File['Event'].unique()] + ['All'])
        self.b = b
        self.as_Csv.triggered.connect(self.saveASCSV)
        self.events.activated.connect(self.drowew)
        self.drownowevent(Event, File)
        self.znach.setText(f"Zanch: {b.znach}")
        self.drowew()

    def drowew(self):
        global File
        if self.events.currentText() == "All":
            plot_data = File[(File['ch'] == self.b.pin) & (File['SIPM'] == self.b.sipm)]
            x = range(0,1024)
            for i in File['Event'].unique():
                y = plot_data[plot_data['Event'] == i].iloc[0][5:]
                plt.plot(x, y)
            plt.savefig('0.png', bbox_inches='tight')
            plt.clf()
            self.pixmap = QPixmap('0.png')
            self.label_2.setPixmap(self.pixmap)
            self.label_2.resize(self.pixmap.width(), self.pixmap.height())
            self.label_2.move(100, 400)
        else:
            plot_data = File[((File['Event'] == int(self.events.currentText()))&(File['ch'] == self.b.pin)&(File['SIPM'] == self.b.sipm))]
            print(plot_data.head())
            y = plot_data.iloc[0][5:].tolist()
            x = range(0,1024)
            plt.figure(figsize=(7,4))
            plt.plot(x, y)
            plt.savefig('0.png', bbox_inches='tight')
            plt.clf()
            self.pixmap = QPixmap('0.png')
            self.label_2.setPixmap(self.pixmap)
            self.label_2.resize(self.pixmap.width(), self.pixmap.height())
            self.label_2.move(100, 400)

    def saveASCSV(self):
        file = SaveFileDiolog=QtGui.QFileDiolog.getSaveFileName(parent=None, caption="Заголовок окна", 
         directory="file:///c:\\Python34", 
          filter="All (*);;py (*.py *.pyw)", 
          initialFilter="py (*.py *.pyw)")
        fileName = file[0].toLocalFile()


    def drownowevent(self, Event, File):
        print(File.head())
        print(Event)
        print(self.b.pin)
        print(self.b.sipm)
        plot_data = File[((File['Event'] == int(Event))&(File['ch'] == self.b.pin)&(File['SIPM'] == self.b.sipm))]
        print(plot_data.head())
        y = plot_data.iloc[0][5:].tolist()
        x = range(0,1024)
        plt.figure(figsize=(7,4))
        plt.plot(x, y)
        plt.savefig('0.png', bbox_inches='tight')
        plt.clf()
        self.pixmap = QPixmap('0.png')
        self.label.setPixmap(self.pixmap)
        self.label.resize(self.pixmap.width(), self.pixmap.height())
        self.label.move(100, 2)
        self.nowevent.move(10, 200)
        self.events.move(10, 400)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
