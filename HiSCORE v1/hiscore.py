import sys
import os
import configparser
import time
import pandas as pd

import colorsys
from PyQt6 import uic  # Импортируем uic
from PyQt6.QtWidgets import QApplication, QDialog, QFileDialog, QMainWindow, QVBoxLayout, QLabel, QMenu, QPushButton, QWidget, QComboBox, QSpinBox, QDoubleSpinBox, QCheckBox, QMessageBox, QSlider, QPlainTextEdit, QTextBrowser, QHBoxLayout, QGroupBox
from PyQt6.QtGui import QPixmap, QFont, QAction
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QObject, QThread, pyqtSignal as Signal, pyqtSlot as Slot, Qt

from matplotlib.colors import Normalize
from matplotlib.patches import RegularPolygon, Rectangle
import numpy as np
import matplotlib.cm as cm
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class WorkerAutoPlayer(QObject):
    progress = Signal(int)
    completed = Signal(int)
    
    def __init__(self, p):
        super(WorkerAutoPlayer, self).__init__()
        self.dady = p
        self.q = True
        self.i = 1

    @Slot(int)
    def do_work(self, n):
        while self.q:
            time.sleep(5 / self.dady.sliderAutoPlayer.value())
            self.progress.emit(self.i)
            print(self.q)
            self.i+=1
            time.sleep(5 / self.dady.sliderAutoPlayer.value())
            if self.i > n:
                self.i = 1
            

        if self.q:
            self.completed.emit(self.i)

    def stop(self):
        self.q = False
        self.completed.emit(self.i-1)


class Appp(QMainWindow):
    work_requested = Signal(int)

    resized = Signal()

    def __init__(self):
        super().__init__()
        #global buttonsHW, moveX, moveY
	
        self.setWindowTitle("HISCORE")
        self.setMinimumWidth(650)
        self.setMinimumHeight(450)

        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.resized.connect(self.newSize)

        self._createMenuBar()

        self.box_of_events = QComboBox(self)
        self.box_of_events.move(10, 30)
        self.box_of_events.setFixedSize(90, 20)
        self.box_of_events.activated.connect(self.boxEventwasChanged)

        self.buttonleft = QPushButton('<-', self)
        self.buttonleft.clicked.connect(self.btnL)
        self.buttonleft.setFixedSize(30, 30)
        #self.buttonleft.hide()

        self.buttonright = QPushButton('->', self)
        self.buttonright.clicked.connect(self.btnR)
        self.buttonright.setFixedSize(30, 30)
        #self.buttonright.hide()

        self.directory_of_ustanovki = ''
        self.file_name = ''
        
        config = configparser.ConfigParser()

        if os.path.exists('hiconfig.ini') is not True:
            print(9)
            config = self.DefultSettings()
            with open('hiconfig.ini', 'w') as config_file:
                config.write(config_file)

        config.read('hiconfig.ini')
        self.settings = config

        self.buttons = []
        coords = pd.read_csv('c.dat', names=['ch', 'x', 'y', 'z'], sep='\s+')
        print(coords.head())
        #self.theme.addItems(['magma', 'Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Grays', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'crest', 'crest_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'flare', 'flare_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_grey', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gist_yerg', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'grey', 'hot', 'hot_r', 'hsv', 'hsv_r', 'icefire', 'icefire_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'mako', 'mako_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'rocket', 'rocket_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'vlag', 'vlag_r', 'winter', 'winter_r'])
        for ch, x, y, z in zip(coords['ch'], coords['x'], coords['y'], coords['z']):
            but = QPushButton(f'{ch}', self)
            if ch < 100:
                but.sipm = 1
            elif ch < 200:
                but.sipm = 2
            elif ch < 300:
                but.sipm = 3
            else:
                but.sipm = 4
            but.x = -y
            but.y = -x
            but.z = z
            but.ch = ch
            but.f = False
            but.move(int(x*10), int(y*10))
            but.textcol = 'White'
            but.znach = None
            but.clicked.connect(self.openAdditWin)
            but.win = []
            if but.sipm == 2:
                but.col = '#000000'
                but.colb = '#000000'
            elif but.sipm == 1:
                but.col = '#1f75fe'
                but.colb = '#1f75fe'
            elif but.sipm == 3:
                but.col = '#006400'
                but.colb = '#006400'
            else:
                but.col = '#c35831'
                but.colb = '#c35831'
            self.buttons.append(but)
        self.coords = coords

        self.filenameText = QLabel('None', self)
        self.filenameText.move(40, 40)
        self.filenameText.setFixedWidth(500)

        self.directorynameText = QLabel('None', self)
        self.directorynameText.move(40, 60)
        self.directorynameText.setFixedWidth(500)

        self.timeofeventText = QLabel('None', self)
        self.timeofeventText.move(10, 80)
        self.timeofeventText.setFixedSize(500, 500)

        self.savedfset = QPushButton('Save dir and\nfilename in config', self)
        self.savedfset.move(10, 100)
        self.savedfset.setFixedSize(120, 40)
        self.savedfset.clicked.connect(self.savedffunc)

        self.workerAutoPlayer = WorkerAutoPlayer(self)
        self.workerAutoPlayer_thread = QThread()

        self.workerAutoPlayer.progress.connect(self.update_progress)
        self.workerAutoPlayer.completed.connect(self.complete)

        self.work_requested.connect(self.workerAutoPlayer.do_work)

        self.btn_start = QPushButton('Start', self, clicked=self.stratAutoPlayer)
        self.btn_start.move(10, 120)
        self.btn_start.setFixedSize(60, 25)
        self.btn_stop = QPushButton('Stop', self, clicked=lambda: self.workerAutoPlayer.stop())
        self.btn_stop.move(10, 140)
        self.btn_stop.setFixedSize(60, 25)

        self.workerAutoPlayer.moveToThread(self.workerAutoPlayer_thread)

        self.sliderAutoPlayer = QSlider(self)
        self.sliderAutoPlayer.setOrientation(Qt.Orientation.Horizontal) 
        self.sliderAutoPlayer.move(10, 150)
        self.sliderAutoPlayer.setRange(10,100)
        self.sliderAutoPlayer.setFixedSize(60, 25)

        # start the thread
        self.workerAutoPlayer_thread.start()

        self.i = -1


        self.check()

    def stratAutoPlayer(self):
        if self.file_name == "":
            return None
        self.btn_start.setEnabled(False)
        n = 5
        self.workerAutoPlayer.i = int(self.box_of_events.currentText())
        self.workerAutoPlayer.q = True
        self.work_requested.emit(self.len_of_events)

    def update_progress(self, s):
        self.box_of_events.setCurrentText(str(s))
        self.boxEventwasChanged()

    def complete(self, s):
        self.box_of_events.setCurrentText(str(s))
        self.btn_start.setEnabled(True)

    def check(self):

        if self.settings.get('Set_path', 'directory') != 'None':
            if os.path.exists(self.settings.get('Set_path', 'directory')) is not True:
                QMessageBox.about(self, "Error", "Папки указанной в настройках не сущетвует")
            else:
                self.directory_of_ustanovki = self.settings.get('Set_path', 'directory')
                self.directorynameText.setText(f'directory: {self.directory_of_ustanovki}')

        if self.settings.get('Set_path', 'filename') != 'None':
            if os.path.exists(self.settings.get('Set_path', 'filename')) is not True:
                QMessageBox.about(self, "Error", "Файла указанного в настройках не сущетвует")
            else:
                self.openingFile(self.settings.get('Set_path', 'filename'))
                self.file_name = self.settings.get('Set_path', 'filename')
                self.boxEventwasChanged()

    def savedffunc(self):
        self.settings.set('Set_path', 'directory', f'{self.directory_of_ustanovki}')
        self.settings.set('Set_path', 'filename', f'{self.file_name}')
        with open('hiconfig.ini', 'w') as config_file:
            self.settings.write(config_file)

    def btnR(self):
        if self.file_name == "":
            return None
        s = int(self.box_of_events.currentText())
        s += 1
        if s > self.len_of_events:
            s = 1
        print(s)
        self.box_of_events.setCurrentText(str(s))
        self.boxEventwasChanged()

    def btnL(self):
        if self.file_name == "":
            return None
        s = int(self.box_of_events.currentText())
        s -= 1
        if s < 1:
            s = self.len_of_events
        self.box_of_events.setCurrentText(str(s))
        self.boxEventwasChanged()
        

    def _createMenuBar(self):
        menuBar = self.menuBar()

        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        self.openFile = QAction("&Open file...", self)
        #self.saveasPng = QAction("&Save as PNG", self)

        self.openFile.triggered.connect(self.OpenF)
        #self.saveasPng.triggered.connect(self.SavePng)
        self.openDirectory = QAction('&Open Directory...', self)

        self.openDirectory.triggered.connect(self.OpenD)

        fileMenu.addAction(self.openFile)
        fileMenu.addAction(self.openDirectory)
        #fileMenu.addAction(self.saveasPng)
        '''
        editMenu = menuBar.addMenu("&Settings")
        self.setVisual = QAction("&SetVisual...", self)
        self.setVisual.triggered.connect(self.openVisualwin)
        editMenu.addAction(self.setVisual)

        helpMenu = menuBar.addMenu("&Help")
        self.sprafka = QAction("&Reference...", self)
        self.sprafka.triggered.connect(self.openReference)
        helpMenu.addAction(self.sprafka)'''

    def DefultSettings(self):
        config = configparser.ConfigParser()
        config.add_section('Set_SIMPS')
        config.set('Set_SIMPS', 'buttonsHW', '16.22')
        config.set('Set_SIMPS', 'moveX', '99.99')
        config.set('Set_SIMPS', 'moveY', '99.99')
        config.set('Set_SIMPS', 'movingX', '-9')
        config.set('Set_SIMPS', 'movingY', '15')
        config.add_section('Set_theme')
        config.set('Set_theme', 'theme', 'Blues')
        config.add_section('Set_HStext')
        config.set('Set_HStext', 'HZnach', '1')
        config.set('Set_HStext', 'HSipm', '1')
        config.set('Set_HStext', 'HChan', '1')
        config.add_section('Set_bord')
        config.set('Set_bord', 'st', '200')
        config.set('Set_bord', 'la', '270')
        config.add_section('Set_path')
        config.set('Set_path', 'directory', 'None')
        config.set('Set_path', 'filename', 'None')


        return config

    def OpenD(self):

        fname = QFileDialog.getExistingDirectory(
            parent=self,
            caption="Select directory",
            #directory=HOME_PATH,
            options=QFileDialog.Option.ShowDirsOnly,
            )
        
        if str(fname) != '':
            self.directory_of_ustanovki = str(fname)
            self.directorynameText.setText(f'directory: {self.directory_of_ustanovki}')
            #self.openingFile(fname)
        else:
            return None   

    def boxEventwasChanged(self):
        self.now_event = self.box_of_events.currentText()
        i = 0
        for j in range(len(self.list_of_events)):
            if self.list_of_events[j][0] != ' ':
                i += 1
            if i == int(self.now_event):
                s = []
                for k in range(int(self.list_of_events[j])):
                    s.append(self.list_of_events[j + k + 1])
                break
        self.list_of_ustanovki = []
        self.events_is_ustanovki = []

        self.timeofeventText.setText('\n'.join([" ".join(i.split()[:3]) for i in s]))
        self.timeofeventText.setFixedHeight(17*len(s))

        for i in s:
            self.list_of_ustanovki.append(i.split()[0])
            self.events_is_ustanovki.append(i.split()[1])
        self.slovar_of_ev_and_us = {}
        for i in s:
            self.slovar_of_ev_and_us[i.split()[0]] = i.split()[1]
        print(self.slovar_of_ev_and_us)
        self.drow()


    def drow(self):
        for i in self.buttons:
            if str(i.ch) in self.list_of_ustanovki:
                i.col = '#2F4F4F'
            else:
                i.col = '#778899'
        self.newSize()
        

    def openAdditWin(self):
        if self.file_name == "":
            return None
        
        b = self.sender()

        if str(b.ch) not in self.slovar_of_ev_and_us:
            return None

        if self.directory_of_ustanovki == '':
            QMessageBox.about(self, "Error", "Не выбрана директория")
            return None
        
        
        res = str(b.ch).rjust(2, '0')
        if  not os.path.exists(self.directory_of_ustanovki + f'/station_{res}.dat'):
            QMessageBox.about(self, "Error", "Нет файла для установки " + f"{res}")
            return None
        print(res)

        #1084

        if str(b.ch) not in self.slovar_of_ev_and_us:
            return None

        f = open(self.directory_of_ustanovki + f'/station_{res}.dat', 'r')
        d = f.readlines()
        f.close()
        ev = self.slovar_of_ev_and_us[str(b.ch)]
        print(ev)
        flag = False
        for i in range(len(d)):
            if d[i][0] in '0123456789':
                if int(d[i].split()[0]) == int(ev):
                    print('Есть')
                    flag = True
                    break

        if flag:
            df = pd.read_csv(self.directory_of_ustanovki + f'/station_{res}.dat', sep="\s+", names=[str(i) for i in range(401)])
            print(df.head(20))
            s = []
            for j in range(9):
                s.append(d[i + j + 1].split()) 
            if not b.f:
                b.win.append(Ustanovka(b, self, df=df, event=int(ev), fn=self.file_name))
                b.win[-1].show()
                b.f = False
            return None
        QMessageBox.about(self, "Error", "В файле установки событие не найдено")
        print('Нет')

    def newSize(self):
        buttonsHW = float(self.settings.get('Set_SIMPS', 'buttonsHW'))
        moveX = float(self.settings.get('Set_SIMPS', 'moveX'))
        moveY = float(self.settings.get('Set_SIMPS', 'moveY'))
        movingX = int(self.settings.get('Set_SIMPS', 'movingX'))
        movingY = int(self.settings.get('Set_SIMPS', 'movingY'))
        

        H = self.centralwidget.frameSize().height()
        W = self.centralwidget.frameSize().width()

        self.btn_start.move(W-65, 25)
        self.btn_stop.move(W-65, 50)
        self.sliderAutoPlayer.move(W-65, 75)

        self.buttonleft.move(W - 65, H - 10)
        self.buttonright.move(W - 35, H - 10)

        #self.timeofeventText.move(10, 20)

        self.savedfset.move(10, H-65)

        S = min(round(H/buttonsHW), round(W/buttonsHW))
        s = min(round(H), round(W))

        #self.buttonright.setFixedSize(round(s**0.52), round(s**0.52))
        #self.buttonleft.setFixedSize(round(s**0.52), round(s**0.52))

        #w = round(W/2)
        #h = round(H/2)
        for i in self.buttons:
            i.setFixedSize(S, S)
            
            i.setStyleSheet(" QPushButton {background-color: " + i.col + " ; color: " + i.textcol +" ; border-radius: "+str(int(i.frameSize().width()/2))+"px; font-size: " +str(int(i.frameSize().width()/4.3))+ "px ; border: 2px solid" + i.colb + "} " # QPushButton:hover { background-color: rgb(16, 16, 24) ; color: rgb(76, 76, 76);}
                                        "QPushButton:pressed {background-color: #b784a7 ; }")
            if i.znach is None:
                i.setText(f'{i.ch}')   
            else:
                if self.HZnach and self.HChan and not self.HSipm:
                    i.setText(f'{int(i.znach)}\nCh:{i.ch}') 
                else:
                    k = str(str(int(i.znach)) + str("\n" if self.HSipm else "") if self.HZnach else "") + str("SIPM:" + str(i.sipm) + str("\n" if self.HChan else "") if self.HSipm else "") + str("Ch:" + str(i.ch) if self.HChan else "")
                    i.setText(k)   
            i.move(round((i.x - 250) * S / moveX) + W // 2+movingX, round((i.y) * S / moveY)+ H // 2 + movingY)

        self.filenameText.move(20, H - 30)
        self.directorynameText.move(20, H - 10)
            
    def OpenF(self):
        '''
        fname = QFileDialog.getExistingDirectory(
            parent=self,
            #caption="Select directory",
            #directory=HOME_PATH,
            #options=QFileDialog.Option.ShowDirsOnly,
            )'''
        
        fname = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")

        
        if fname[0] != '':
            self.openingFile(fname[0])
            self.file_name = fname[0]
            self.boxEventwasChanged()
        else:
            return None
        
    def openingFile(self, a):
        f = open(a, 'r')
        try:
            self.list_of_events = f.readlines()
            f.close()
            i = 0
            for j in range(len(self.list_of_events)):
                if self.list_of_events[j][0] != ' ':
                    i += 1
            self.len_of_events = i
            self.box_of_events.addItems([str(j) for j in range(1, i+1)])
            self.filenameText.setText(f'file name: {a}')
        except:
            print('fuck')
    
    
    def resizeEvent(self, event):
        self.resized.emit()
        return super(Appp, self).resizeEvent(event)
    
class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.tight_layout()
        fig.subplots_adjust(left=0.08, right=0.995, top=0.955, bottom=0.160)
        #fig.subplots_adjust(left=0.020, right=0.980, top=0.950, bottom=0.090)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class WorkerAutoPlayerUs(QObject):
    progress = Signal(int)
    completed = Signal(int)
    
    def __init__(self, p, ind):
        super(WorkerAutoPlayerUs, self).__init__()
        self.dady = p
        self.q = True
        self.i = ind

    @Slot(int)
    def do_work(self, ma):
        if ma>0:
            while self.q:
                time.sleep(10 / self.dady.sliderAutoPlayerUs.value())
                
                print(self.q)
                self.i+=10
                
                if self.i >= ma:
                    self.i = 0
                self.progress.emit(self.i)
                time.sleep(10 / self.dady.sliderAutoPlayerUs.value())
        
        else:
            while self.q:
                time.sleep(10 / self.dady.sliderAutoPlayerUs.value())
                print(self.q)
                self.i-=10
                if self.i < 0:
                    self.i = -1*ma-10
                self.progress.emit(self.i)
                time.sleep(10 / self.dady.sliderAutoPlayerUs.value())
            

        if self.q:
            if ma > 0:
                if self.i == 0:
                    self.completed.emit(ma-10)
                else:
                    self.completed.emit(self.i - 10)
            else:
                if self.i == -1*ma-10:
                    self.completed.emit(0)
                else:
                    self.completed.emit(self.i+10)

    def stop(self):
        self.q = False
        self.completed.emit(self.i)
    
class Ustanovka(QMainWindow):
    work_requested = Signal(int)

    resized = QtCore.pyqtSignal()
    
    def __init__(self, b, parent, df, event, fn):
        
        super().__init__()
        self.setMinimumWidth(600)
        self.setMinimumHeight(450)
        

        self.parent = parent
        self.b = b
        self.df=df
        self.ev = event
        self.fn = fn

        #self.worker

        #print(len(s[0]))
        print(event)

        self.index = df.index[df['0']== str(event)].tolist()[0]
        print(df.loc[self.index])

        self.workerAutoPlayerUs = WorkerAutoPlayerUs(self, self.index)
        self.workerAutoPlayer_threadUs = QThread()

        self.workerAutoPlayerUs.progress.connect(self.update_progress)
        self.workerAutoPlayerUs.completed.connect(self.complete)

        self.work_requested.connect(self.workerAutoPlayerUs.do_work)

        self.btn_startr = QPushButton('>>', self, clicked=self.startAutoPlayerUsR)
        self.btn_startr.move(10, 120)
        #self.btn_startr.setFixedSize(60, 25)
        self.btn_startl = QPushButton('<<', self, clicked=self.startAutoPlayerUsL)
        self.btn_startl.move(10, 120)
        #self.btn_startl.setFixedSize(60, 25)
        self.btn_stop = QPushButton('Stop', self, clicked=lambda: self.workerAutoPlayerUs.stop())
        self.btn_stop.move(10, 140)
        #self.btn_stop.setFixedSize(60, 25)

        self.workerAutoPlayerUs.moveToThread(self.workerAutoPlayer_threadUs)

        self.sliderAutoPlayerUs = QSlider(self)
        self.sliderAutoPlayerUs.setOrientation(Qt.Orientation.Horizontal) 
        self.sliderAutoPlayerUs.move(10, 150)
        self.sliderAutoPlayerUs.setRange(10,100)
        #self.sliderAutoPlayerUs.setFixedSize(60, 25)

        # start the thread
        self.workerAutoPlayer_threadUs.start()

        lay1 = QVBoxLayout()

        '''

        self.ba1 = QPushButton(self)
        self.ba1.setFixedSize(25, 25)

        self.ba2 = QPushButton(self)
        self.ba2.setFixedSize(25, 25)
        

        hay1 = QHBoxLayout()
        hay1.addWidget(self.ba1)
        hay1.addWidget(self.ba2)   

        self.ba3 = QPushButton(self)
        self.ba3.setFixedSize(25, 25)

        self.ba4 = QPushButton(self)
        self.ba4.setFixedSize(25, 25)

        hay2 = QHBoxLayout()
        hay2.addWidget(self.ba3)
        hay2.addWidget(self.ba4)   

        self.bd1 = QPushButton(self)
        self.bd1.setFixedSize(25, 25)

        self.bd2 = QPushButton(self)
        self.bd2.setFixedSize(25, 25)
        
        hay3 = QHBoxLayout()
        hay3.addWidget(self.bd1)
        hay3.addWidget(self.bd2)   

        self.bd3 = QPushButton(self)
        self.bd3.setFixedSize(25, 25)

        self.bd4 = QPushButton(self)
        self.bd4.setFixedSize(25, 25)

        hay4 = QHBoxLayout()
        hay4.addWidget(self.bd3)
        hay4.addWidget(self.bd4)  ''' 

        self.sc1 = MplCanvas(self, width=5, height=4, dpi=100)

        toolbar1 = NavigationToolbar(self.sc1, self)

        self.sc2 = MplCanvas(self, width=5, height=4, dpi=100)

        toolbar2 = NavigationToolbar(self.sc2, self)

        self.sc3 = MplCanvas(self, width=5, height=4, dpi=100)

        toolbar3 = NavigationToolbar(self.sc3, self)

        self.sc1.axes.set_xlabel('time')

        #lay1.addWidget(QLabel('Анодный сигнал'))
        #lay1.addLayout(hay1)
        #lay1.addLayout(hay2)
        #lay1.addWidget(QLabel('Диодный сигнал'))
        #lay1.addLayout(hay3)
        #lay1.addLayout(hay4)

        '''

        self.sq = QSpinBox(self)
        self.sq.setMinimum(1)
        self.sq.setMaximum(400)
        self.sq.valueChanged.connect(self.setRate1)

        self.thr1 = QThread()
        self.thr1.start()

        self.wk1 = WorkerPD(self)
        self.wk1.moveToThread(self.thr1)
        self.wk1.stepIncreased.connect(self.sq.setValue)

        self.sqsta = QPushButton(self)
        self.sqsta.clicked.connect(lambda: self.wk1.stop())
        self.sqsto = QPushButton(self)
        self.sqsto.clicked.connect(self.wk1.task)


        hay7 = QHBoxLayout()
        hay7.addWidget(self.sq)
        hay7.addWidget(self.sqsta)
        hay7.addWidget(self.sqsto)

        lay1.addLayout(hay7)

        '''
        
        self.w = QWidget()
        self.w.setFixedSize(50, 300)

        lay1.addWidget(self.w)

        self.ba = QComboBox(self)
        self.ba.addItems(['a1', 'a2', 'a3', 'a4', 'Все'])
        self.ba.activated.connect(self.fq1)
        self.bd = QComboBox(self)
        self.bd.addItems(['d1', 'd2', 'd3', 'd4', 'Все'])
        self.bd.activated.connect(self.fq2)

        lay5 = QVBoxLayout()

        hay6 = QHBoxLayout()
        hay6.addWidget(toolbar1)
        hay6.addWidget(self.ba)

        hay7 = QHBoxLayout()
        hay7.addWidget(toolbar2)
        hay7.addWidget(self.bd)

        lay5.addLayout(hay6)
        lay5.addWidget(self.sc1)
        lay5.addLayout(hay7)
        lay5.addWidget(self.sc2)
        lay5.addWidget(toolbar3)
        lay5.addWidget(self.sc3)
        #layout.addLayout(self.Hl)



        #self.minIndex = int(min(df['0']))
        #self.maxIndex = int(max(df['0']))


        #print(self.minIndex)

        q = self.df.loc[self.index].to_list()
        self.ev = q[0]
        self.time = q[1]
        self.setWindowTitle(f"{self.ev} {self.time} {self.fn}")

        self.a1 = list(map(int, df.loc[self.index+1].to_list()[1:]))
        self.a2 = list(map(int, df.loc[self.index+2].to_list()[1:]))
        self.a3 = list(map(int, df.loc[self.index+3].to_list()[1:]))
        self.a4 = list(map(int, df.loc[self.index+4].to_list()[1:]))

        self.d1 = list(map(int, df.loc[self.index+5].to_list()[1:]))
        self.d2 = list(map(int, df.loc[self.index+6].to_list()[1:]))
        self.d3 = list(map(int, df.loc[self.index+7].to_list()[1:]))
        self.d4 = list(map(int, df.loc[self.index+8].to_list()[1:]))

        self.tr1 = list(map(int, df.loc[self.index+9].to_list()[1:]))

        self.setRate()

        self.f1()
        self.f2()
        self.tr()

        self.btn_r = QPushButton('->', self, clicked=self.rightB)
        self.btn_l = QPushButton('<-', self, clicked=self.leftB)

        lay2 = QHBoxLayout()
        lay2.addWidget(self.btn_startl)
        lay2.addWidget(self.btn_l)
        lay2.addWidget(self.btn_stop)
        lay2.addWidget(self.btn_r)
        
        lay2.addWidget(self.btn_startr)
        
        lay2.addWidget(self.sliderAutoPlayerUs)

        lay5.addLayout(lay2)

        hay5 = QHBoxLayout()
        #hay5.addLayout(lay1)
        hay5.addLayout(lay5)
        #hay5.addLayout(lay2)

        widget = QWidget()
        widget.setLayout(hay5)

        self.centralwidget = widget
        self.setCentralWidget(widget)
        self.resized.connect(self.newSize)

    def startAutoPlayerUsR(self):
        self.workerAutoPlayerUs.stop()
        print(self.index)
        self.btn_startr.setEnabled(False)
        self.btn_startl.setEnabled(False)
        
        n = 5
        self.workerAutoPlayerUs.i = self.index
        self.workerAutoPlayerUs.q = True
        self.work_requested.emit(len(self.df))

    def startAutoPlayerUsL(self):
        self.workerAutoPlayerUs.stop()
        self.btn_startl.setEnabled(False)
        self.btn_startr.setEnabled(False)
        
        n = 5
        self.workerAutoPlayerUs.i = self.index
        self.workerAutoPlayerUs.q = True
        self.work_requested.emit(len(self.df) * -1)

    def update_progress(self, s):
        self.index = s
        print(self.index)
        q = self.df.loc[self.index].to_list()
        self.ev = q[0]
        self.time = q[1]
        self.setWindowTitle(f"{self.ev} {self.time} {self.fn}")

        self.a1 = list(map(int, self.df.loc[self.index+1].to_list()[1:]))
        self.a2 = list(map(int, self.df.loc[self.index+2].to_list()[1:]))
        self.a3 = list(map(int, self.df.loc[self.index+3].to_list()[1:]))
        self.a4 = list(map(int, self.df.loc[self.index+4].to_list()[1:]))

        self.d1 = list(map(int, self.df.loc[self.index+5].to_list()[1:]))
        self.d2 = list(map(int, self.df.loc[self.index+6].to_list()[1:]))
        self.d3 = list(map(int, self.df.loc[self.index+7].to_list()[1:]))
        self.d4 = list(map(int, self.df.loc[self.index+8].to_list()[1:]))

        self.tr1 = list(map(int, self.df.loc[self.index+9].to_list()[1:]))

        self.fq1()
        self.fq2()
        self.tr()

    def complete(self, s):
        print(s)
        self.index = s
        q = self.df.loc[self.index].to_list()
        self.ev = q[0]
        self.time = q[1]
        self.setWindowTitle(f"{self.ev} {self.time} {self.fn}")

        self.a1 = list(map(int, self.df.loc[self.index+1].to_list()[1:]))
        self.a2 = list(map(int, self.df.loc[self.index+2].to_list()[1:]))
        self.a3 = list(map(int, self.df.loc[self.index+3].to_list()[1:]))
        self.a4 = list(map(int, self.df.loc[self.index+4].to_list()[1:]))

        self.d1 = list(map(int, self.df.loc[self.index+5].to_list()[1:]))
        self.d2 = list(map(int, self.df.loc[self.index+6].to_list()[1:]))
        self.d3 = list(map(int, self.df.loc[self.index+7].to_list()[1:]))
        self.d4 = list(map(int, self.df.loc[self.index+8].to_list()[1:]))

        self.tr1 = list(map(int, self.df.loc[self.index+9].to_list()[1:]))

        self.fq1()
        self.fq2()
        self.tr()
        self.btn_startr.setEnabled(True)
        self.btn_startl.setEnabled(True)

    def rightB(self):
        if self.index + 10 >= len(self.df):
            self.index = 0
        else:
            self.index += 10

        q = self.df.loc[self.index].to_list()
        self.ev = q[0]
        self.time = q[1]
        self.setWindowTitle(f"{self.ev} {self.time} {self.fn}")

        self.a1 = list(map(int, self.df.loc[self.index+1].to_list()[1:]))
        self.a2 = list(map(int, self.df.loc[self.index+2].to_list()[1:]))
        self.a3 = list(map(int, self.df.loc[self.index+3].to_list()[1:]))
        self.a4 = list(map(int, self.df.loc[self.index+4].to_list()[1:]))

        self.d1 = list(map(int, self.df.loc[self.index+5].to_list()[1:]))
        self.d2 = list(map(int, self.df.loc[self.index+6].to_list()[1:]))
        self.d3 = list(map(int, self.df.loc[self.index+7].to_list()[1:]))
        self.d4 = list(map(int, self.df.loc[self.index+8].to_list()[1:]))

        self.tr1 = list(map(int, self.df.loc[self.index+9].to_list()[1:]))

        self.fq1()
        self.fq2()
        self.tr()
        pass

    def leftB(self):
        if self.index - 9 < 0:
            self.index = len(self.df)-10
        else:
            self.index -= 10

        q = self.df.loc[self.index].to_list()
        self.ev = q[0]
        self.time = q[1]
        self.setWindowTitle(f"{self.ev} {self.time} {self.fn}")

        self.a1 = list(map(int, self.df.loc[self.index+1].to_list()[1:]))
        self.a2 = list(map(int, self.df.loc[self.index+2].to_list()[1:]))
        self.a3 = list(map(int, self.df.loc[self.index+3].to_list()[1:]))
        self.a4 = list(map(int, self.df.loc[self.index+4].to_list()[1:]))

        self.d1 = list(map(int, self.df.loc[self.index+5].to_list()[1:]))
        self.d2 = list(map(int, self.df.loc[self.index+6].to_list()[1:]))
        self.d3 = list(map(int, self.df.loc[self.index+7].to_list()[1:]))
        self.d4 = list(map(int, self.df.loc[self.index+8].to_list()[1:]))

        self.tr1 = list(map(int, self.df.loc[self.index+9].to_list()[1:]))

        self.fq1()
        self.fq2()
        self.tr()
        pass

    def setRate1(self):
        '''
        cmap = cm.get_cmap()
        norm = Normalize(vmin=min(self.a1), vmax=max(self.a1))
        rgba_values = cmap(norm(self.a1))
        if (sum(rgba_values[0]) - 1) / 3 < 0.5:
            self.ba1.textcol = matplotlib.colors.rgb2hex((1, 1, 1))
        else:
            self.ba1.textcol = matplotlib.colors.rgb2hex((0, 0, 0))
                    #i.textcol = matplotlib.colors.rgb2hex((s - r, s - g, s - b))
        self.ba1.col = matplotlib.colors.rgb2hex(rgba_values[self.sq.value() - 1])

        cmap = cm.get_cmap()
        norm = Normalize(vmin=min(self.a4), vmax=max(self.a4))
        rgba_values = cmap(norm(self.a4))
        if (sum(rgba_values[self.sq.value() - 1]) - 1) / 3 < 0.5:
            self.ba4.textcol = matplotlib.colors.rgb2hex((1, 1, 1))
        else:
            self.ba4.textcol = matplotlib.colors.rgb2hex((0, 0, 0))
                    #i.textcol = matplotlib.colors.rgb2hex((s - r, s - g, s - b))
        self.ba4.col = matplotlib.colors.rgb2hex(rgba_values[self.sq.value() - 1])

        cmap = cm.get_cmap()
        norm = Normalize(vmin=min(self.a2), vmax=max(self.a2))
        rgba_values = cmap(norm(self.a2))
        if (sum(rgba_values[self.sq.value() - 1]) - 1) / 3 < 0.5:
            self.ba2.textcol = matplotlib.colors.rgb2hex((1, 1, 1))
        else:
            self.ba2.textcol = matplotlib.colors.rgb2hex((0, 0, 0))
                    #i.textcol = matplotlib.colors.rgb2hex((s - r, s - g, s - b))
        self.ba2.col = matplotlib.colors.rgb2hex(rgba_values[self.sq.value() - 1])

        cmap = cm.get_cmap()
        norm = Normalize(vmin=min(self.a3), vmax=max(self.a3))
        rgba_values = cmap(norm(self.a3))
        if (sum(rgba_values[self.sq.value() - 1]) - 1) / 3 < 0.5:
            self.ba3.textcol = matplotlib.colors.rgb2hex((1, 1, 1))
        else:
            self.ba3.textcol = matplotlib.colors.rgb2hex((0, 0, 0))
                    #i.textcol = matplotlib.colors.rgb2hex((s - r, s - g, s - b))
        self.ba3.col = matplotlib.colors.rgb2hex(rgba_values[self.sq.value() - 1])


        cmap = cm.get_cmap()
        norm = Normalize(vmin=min(self.d1), vmax=max(self.d1))
        rgba_values = cmap(norm(self.d1))
        if (sum(rgba_values[0]) - 1) / 3 < 0.5:
            self.bd1.textcol = matplotlib.colors.rgb2hex((1, 1, 1))
        else:
            self.bd1.textcol = matplotlib.colors.rgb2hex((0, 0, 0))
                    #i.textcol = matplotlib.colors.rgb2hex((s - r, s - g, s - b))
        self.bd1.col = matplotlib.colors.rgb2hex(rgba_values[self.sq.value() - 1])

        cmap = cm.get_cmap()
        norm = Normalize(vmin=min(self.d4), vmax=max(self.d4))
        rgba_values = cmap(norm(self.d4))
        if (sum(rgba_values[self.sq.value() - 1]) - 1) / 3 < 0.5:
            self.bd4.textcol = matplotlib.colors.rgb2hex((1, 1, 1))
        else:
            self.bd4.textcol = matplotlib.colors.rgb2hex((0, 0, 0))
                    #i.textcol = matplotlib.colors.rgb2hex((s - r, s - g, s - b))
        self.bd4.col = matplotlib.colors.rgb2hex(rgba_values[self.sq.value() - 1])

        cmap = cm.get_cmap()
        norm = Normalize(vmin=min(self.d2), vmax=max(self.d2))
        rgba_values = cmap(norm(self.d2))
        if (sum(rgba_values[self.sq.value() - 1]) - 1) / 3 < 0.5:
            self.bd2.textcol = matplotlib.colors.rgb2hex((1, 1, 1))
        else:
            self.bd2.textcol = matplotlib.colors.rgb2hex((0, 0, 0))
                    #i.textcol = matplotlib.colors.rgb2hex((s - r, s - g, s - b))
        self.bd2.col = matplotlib.colors.rgb2hex(rgba_values[self.sq.value() - 1])

        cmap = cm.get_cmap()
        norm = Normalize(vmin=min(self.d3), vmax=max(self.d3))
        rgba_values = cmap(norm(self.d3))
        if (sum(rgba_values[self.sq.value() - 1]) - 1) / 3 < 0.5:
            self.bd3.textcol = matplotlib.colors.rgb2hex((1, 1, 1))
        else:
            self.bd3.textcol = matplotlib.colors.rgb2hex((0, 0, 0))
                    #i.textcol = matplotlib.colors.rgb2hex((s - r, s - g, s - b))
        self.bd3.col = matplotlib.colors.rgb2hex(rgba_values[self.sq.value() - 1])



        self.ba1.textq = self.a1[self.sq.value() - 1]
        self.ba2.textq = self.a2[self.sq.value() - 1]
        self.ba3.textq = self.a3[self.sq.value() - 1]
        self.ba4.textq = self.a4[self.sq.value() - 1]

        self.bd1.textq = self.d1[self.sq.value() - 1]
        self.bd2.textq = self.d2[self.sq.value() - 1]
        self.bd3.textq = self.d3[self.sq.value() - 1]
        self.bd4.textq = self.d4[self.sq.value() - 1]

        self.f1(self.sq.value() - 1)
        self.f2(self.sq.value() - 1)
        '''

        self.newSize()




    def setRate(self):
        pass
    '''

        Ma1 = max(self.a1)
        Ma2 = max(self.a2)
        Ma3 = max(self.a3)
        Ma4 = max(self.a4)

        Md1 = max(self.d1)
        Md2 = max(self.d2)
        Md3 = max(self.d3)
        Md4 = max(self.d4)


        self.ba1.textq = Ma1
        self.ba2.textq = Ma2
        self.ba3.textq = Ma3
        self.ba4.textq = Ma4

        self.bd1.textq = Md1
        self.bd2.textq = Md2
        self.bd3.textq = Md3
        self.bd4.textq = Md4


        cmap = cm.get_cmap()

        MA = [Ma1, Ma2, Ma3, Ma4]
        MD = [Md1, Md2, Md3, Md4]

        norm = Normalize(vmin=min(MA), vmax=max(MA))
        rgba_values = cmap(norm(MA))


        if (sum(rgba_values[0]) - 1) / 3 < 0.5:
            self.ba1.textcol = matplotlib.colors.rgb2hex((1, 1, 1))
        else:
            self.ba1.textcol = matplotlib.colors.rgb2hex((0, 0, 0))
                    #i.textcol = matplotlib.colors.rgb2hex((s - r, s - g, s - b))
        self.ba1.col = matplotlib.colors.rgb2hex(rgba_values[0])
        

        if (sum(rgba_values[1]) - 1) / 3 < 0.5:
            self.ba2.textcol = matplotlib.colors.rgb2hex((1, 1, 1))
        else:
            self.ba2.textcol = matplotlib.colors.rgb2hex((0, 0, 0))
                    #i.textcol = matplotlib.colors.rgb2hex((s - r, s - g, s - b))
        self.ba2.col = matplotlib.colors.rgb2hex(rgba_values[1])

        if (sum(rgba_values[2]) - 1) / 3 < 0.5:
            self.ba3.textcol = matplotlib.colors.rgb2hex((1, 1, 1))
        else:
            self.ba3.textcol = matplotlib.colors.rgb2hex((0, 0, 0))
                    #i.textcol = matplotlib.colors.rgb2hex((s - r, s - g, s - b))
        self.ba3.col = matplotlib.colors.rgb2hex(rgba_values[2])

        if (sum(rgba_values[3]) - 1) / 31 < 0.5:
            self.ba4.textcol = matplotlib.colors.rgb2hex((1, 1, 1))
        else:
            self.ba4.textcol = matplotlib.colors.rgb2hex((0, 0, 0))
                    #i.textcol = matplotlib.colors.rgb2hex((s - r, s - g, s - b))
        self.ba4.col = matplotlib.colors.rgb2hex(rgba_values[3])


        cmap = cm.get_cmap()

        norm = Normalize(vmin=min(MD), vmax=max(MD))
        rgba_values = cmap(norm(MD))

        if (sum(rgba_values[0]) - 1) / 3 < 0.5:
            self.bd1.textcol = matplotlib.colors.rgb2hex((1, 1, 1))
        else:
            self.bd1.textcol = matplotlib.colors.rgb2hex((0, 0, 0))
                    #i.textcol = matplotlib.colors.rgb2hex((s - r, s - g, s - b))
        self.bd1.col = matplotlib.colors.rgb2hex(rgba_values[0])

        if (sum(rgba_values[1]) - 1) / 3 < 0.5:
            self.bd2.textcol = matplotlib.colors.rgb2hex((1, 1, 1))
        else:
            self.bd2.textcol = matplotlib.colors.rgb2hex((0, 0, 0))
                    #i.textcol = matplotlib.colors.rgb2hex((s - r, s - g, s - b))
        self.bd2.col = matplotlib.colors.rgb2hex(rgba_values[1])

        if (sum(rgba_values[2]) - 1) / 3 < 0.5:
            self.bd3.textcol = matplotlib.colors.rgb2hex((1, 1, 1))
        else:
            self.bd3.textcol = matplotlib.colors.rgb2hex((0, 0, 0))
                    #i.textcol = matplotlib.colors.rgb2hex((s - r, s - g, s - b))
        self.bd3.col = matplotlib.colors.rgb2hex(rgba_values[2])

        if (sum(rgba_values[3]) - 1) / 31 < 0.5:
            self.bd4.textcol = matplotlib.colors.rgb2hex((1, 1, 1))
        else:
            self.bd4.textcol = matplotlib.colors.rgb2hex((0, 0, 0))
                    #i.textcol = matplotlib.colors.rgb2hex((s - r, s - g, s - b))
        self.bd4.col = matplotlib.colors.rgb2hex(rgba_values[3])

    '''

    def fq1(self):
        self.f1()

    def fq2(self):
        self.f2()

    def f1(self, q=0):
        self.sc1.axes.cla()

        if self.ba.currentText() == 'Все':
            self.sc1.axes.plot(self.a1, color='blue', label=f"a1")
            self.sc1.axes.plot(self.a2, color='red', label=f"a2")
            self.sc1.axes.plot(self.a3, color='pink', label=f"a3")
            self.sc1.axes.plot(self.a4, color='yellow', label=f"a4")
            if q != 0:
                self.sc1.axes.plot([q, q], [0, max(self.a1 + self.a2 + self.a3 + self.a4)], color='green')
            self.sc1.axes.legend(ncol=1, bbox_to_anchor=(1,1), loc='upper right')
            #self.sc.axes.set_title(f'Event {self.event.currentText()} S{self.b.sipm} C{self.b.ch}')
            self.sc1.axes.grid(linestyle='--', color='pink')
            #self.sc.axes.set_xlim([0, 1023])
            self.sc1.axes.set_xlabel('time')
            self.sc1.axes.set_ylabel('amplitude')
            self.sc1.draw()
            return None


        if self.ba.currentText() == 'a1':
            plot_data = self.a1
            if q != 0:
                self.sc1.axes.plot([q, q], [0, max(self.a1)], color='green')
        elif self.ba.currentText() == 'a2':
            plot_data = self.a2
            if q != 0:
               self.sc1.axes.plot([q, q], [0, max(self.a2)], color='green')
        elif self.ba.currentText() == 'a3':
            plot_data = self.a3
            if q != 0:
                self.sc1.axes.plot([q, q], [0, max(self.a3)], color='green')
        elif self.ba.currentText() == 'a4':
            plot_data = self.a4
            if q != 0:
              self.sc1.axes.plot([q, q], [0, max(self.a4)], color='green')

        

        x = range(0,400)
            #ax.figure(figsize=(7,4))
        self.sc1.axes.plot(plot_data, color='blue')
            #self.sc.axes.set_title(f'Event {self.event.currentText()} S{self.b.sipm} C{self.b.ch}')
        self.sc1.axes.grid(linestyle='--', color='pink')
            #self.sc.axes.set_xlim([0, 1023])
        self.sc1.axes.set_xlabel('time')
        self.sc1.axes.set_ylabel('amplitude')

        self.sc1.draw()

    def f2(self, q=0):
        self.sc2.axes.cla()

        if self.bd.currentText() == 'Все':
            self.sc2.axes.plot(self.d1, color='blue', label=f"d1")
            self.sc2.axes.plot(self.d2, color='red', label=f"d2")
            self.sc2.axes.plot(self.d3, color='pink', label=f"d3")
            self.sc2.axes.plot(self.d4, color='yellow', label=f"d4")
            if q != 0:
                self.sc2.axes.plot([q, q], [0, max(self.d1 + self.d2 + self.d3 + self.d4)], color='green')
            self.sc2.axes.legend(ncol=1, bbox_to_anchor=(1,1), loc='upper right')
            #self.sc.axes.set_title(f'Event {self.event.currentText()} S{self.b.sipm} C{self.b.ch}')
            self.sc2.axes.grid(linestyle='--', color='pink')
            #self.sc.axes.set_xlim([0, 1023])
            self.sc2.axes.set_xlabel('time')
            self.sc2.axes.set_ylabel('amplitude')
            self.sc2.draw()
            return None

        if self.bd.currentText() == 'd1':
            plot_data = self.d1
            if q != 0:
                self.sc2.axes.plot([q, q], [0, max(self.d1)], color='green')
        elif self.bd.currentText() == 'd2':
            plot_data = self.d2
            if q != 0:
                self.sc2.axes.plot([q, q], [0, max(self.d2)], color='green')
        elif self.bd.currentText() == 'd3':
            plot_data = self.d3
            if q != 0:
                self.sc2.axes.plot([q, q], [0, max(self.d3)], color='green')
        elif self.bd.currentText() == 'd4':
            if q != 0:
                q  = self.d4.index(max(self.d4))
            self.sc2.axes.plot([q, q], [0, max(self.d4)], color='green')

        x = range(0,400)
            #ax.figure(figsize=(7,4))
        self.sc2.axes.plot(plot_data, color='blue')
            #self.sc.axes.set_title(f'Event {self.event.currentText()} S{self.b.sipm} C{self.b.ch}')
        self.sc2.axes.grid(linestyle='--', color='pink')
            #self.sc.axes.set_xlim([0, 1023])
        self.sc2.axes.set_xlabel('time')
        self.sc2.axes.set_ylabel('amplitude')

        self.sc2.draw()

            #self.amax.setText(f'{max(y)}')

    def tr(self):
        self.sc3.axes.cla()    
        x = range(0,400)
            #ax.figure(figsize=(7,4))
        self.sc3.axes.plot(self.tr1, color='blue')
            #self.sc.axes.set_title(f'Event {self.event.currentText()} S{self.b.sipm} C{self.b.ch}')
        self.sc3.axes.grid(linestyle='--', color='pink')
            #self.sc.axes.set_xlim([0, 1023])
        self.sc3.axes.set_xlabel('time')
        self.sc3.axes.set_ylabel('amplitude')

        self.sc3.draw()
   

    def resizeEvent(self, event):
        self.resized.emit()
        return super(Ustanovka, self).resizeEvent(event)
    
    def closeEvent(self, event):
        self.b.f = False
    
    def newSize(self):
        H = self.centralwidget.frameSize().height()
        W = self.centralwidget.frameSize().width()

        s = max(round(40 * W  / 600), round(40 * H  / 600))

        '''

        self.ba1.setFixedSize(int(s), int(s))
        self.ba2.setFixedSize(int(s), int(s))
        self.ba3.setFixedSize(int(s), int(s))
        self.ba4.setFixedSize(int(s), int(s))

        self.bd1.setFixedSize(int(s), int(s))
        self.bd2.setFixedSize(int(s), int(s))
        self.bd3.setFixedSize(int(s), int(s))
        self.bd4.setFixedSize(int(s), int(s))

        self.w.setFixedHeight(round(500 * H  / 450))

        self.ba1.setStyleSheet(" QPushButton {background-color: " + self.ba1.col + " ; color: " + self.ba1.textcol +" ; border-radius: "+str(int(self.ba1.frameSize().width()/4))+"px; font-size: " +str(int(self.ba1.frameSize().width()/4))+ "px ;} " # QPushButton:hover { background-color: rgb(16, 16, 24) ; color: rgb(76, 76, 76);}
                            "QPushButton:pressed {background-color: #b784a7 ; }")
        self.ba2.setStyleSheet(" QPushButton {background-color: " + self.ba2.col + " ; color: " + self.ba2.textcol +" ; border-radius: "+str(int(self.ba2.frameSize().width()/4))+"px; font-size: " +str(int(self.ba2.frameSize().width()/4))+ "px ;} " # QPushButton:hover { background-color: rgb(16, 16, 24) ; color: rgb(76, 76, 76);}
                            "QPushButton:pressed {background-color: #b784a7 ; }")
        self.ba3.setStyleSheet(" QPushButton {background-color: " + self.ba3.col + " ; color: " + self.ba3.textcol +" ; border-radius: "+str(int(self.ba3.frameSize().width()/4))+"px; font-size: " +str(int(self.ba3.frameSize().width()/4))+ "px ;} " # QPushButton:hover { background-color: rgb(16, 16, 24) ; color: rgb(76, 76, 76);}
                            "QPushButton:pressed {background-color: #b784a7 ; }")
        self.ba4.setStyleSheet(" QPushButton {background-color: " + self.ba4.col + " ; color: " + self.ba4.textcol +" ; border-radius: "+str(int(self.ba4.frameSize().width()/4))+"px; font-size: " +str(int(self.ba4.frameSize().width()/4))+ "px ;} " # QPushButton:hover { background-color: rgb(16, 16, 24) ; color: rgb(76, 76, 76);}
                            "QPushButton:pressed {background-color: #b784a7 ; }")
        
        self.bd1.setStyleSheet(" QPushButton {background-color: " + self.bd1.col + " ; color: " + self.bd1.textcol +" ; border-radius: "+str(int(self.bd1.frameSize().width()/4))+"px; font-size: " +str(int(self.bd1.frameSize().width()/4))+ "px ;} " # QPushButton:hover { background-color: rgb(16, 16, 24) ; color: rgb(76, 76, 76);}
                            "QPushButton:pressed {background-color: #b784a7 ; }")
        self.bd2.setStyleSheet(" QPushButton {background-color: " + self.bd2.col + " ; color: " + self.bd2.textcol +" ; border-radius: "+str(int(self.bd2.frameSize().width()/4))+"px; font-size: " +str(int(self.bd2.frameSize().width()/4))+ "px ;} " # QPushButton:hover { background-color: rgb(16, 16, 24) ; color: rgb(76, 76, 76);}
                            "QPushButton:pressed {background-color: #b784a7 ; }")
        self.bd3.setStyleSheet(" QPushButton {background-color: " + self.bd3.col + " ; color: " + self.bd3.textcol +" ; border-radius: "+str(int(self.bd3.frameSize().width()/4))+"px; font-size: " +str(int(self.bd3.frameSize().width()/4))+ "px ;} " # QPushButton:hover { background-color: rgb(16, 16, 24) ; color: rgb(76, 76, 76);}
                            "QPushButton:pressed {background-color: #b784a7 ; }")
        self.bd4.setStyleSheet(" QPushButton {background-color: " + self.bd4.col + " ; color: " + self.bd4.textcol +" ; border-radius: "+str(int(self.bd4.frameSize().width()/4))+"px; font-size: " +str(int(self.bd4.frameSize().width()/4))+ "px ;} " # QPushButton:hover { background-color: rgb(16, 16, 24) ; color: rgb(76, 76, 76);}
                            "QPushButton:pressed {background-color: #b784a7 ; }")
        

        self.ba1.setText(f'{self.ba1.textq}')   
        self.ba2.setText(f'{self.ba2.textq}')   
        self.ba3.setText(f'{self.ba3.textq}')   
        self.ba4.setText(f'{self.ba4.textq}')   

        self.bd1.setText(f'{self.bd1.textq}')   
        self.bd2.setText(f'{self.bd2.textq}')   
        self.bd3.setText(f'{self.bd3.textq}')   
        self.bd4.setText(f'{self.bd4.textq}')   
        '''
        pass

    def closeEvent(self, event):
        self.workerAutoPlayerUs.stop()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Appp()
    ex.show()
    sys.exit(app.exec())