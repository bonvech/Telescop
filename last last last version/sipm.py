import sys
import os
import configparser
import time
import pandas as pd

import colorsys
from PyQt6 import uic  # Импортируем uic
from PyQt6.QtWidgets import QApplication, QDialog, QFileDialog, QMainWindow, QVBoxLayout, QLabel, QMenu, QPushButton, QWidget, QComboBox, QSpinBox, QDoubleSpinBox, QCheckBox, QMessageBox, QSlider
from PyQt6.QtGui import QPixmap, QFont, QAction
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QObject, QThread, pyqtSignal, Qt

from matplotlib.colors import Normalize
from matplotlib.patches import RegularPolygon, Rectangle
import numpy as np
import matplotlib.cm as cm
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt

class WorkerPD(QObject):
    'Object managing the simulation'

    stepIncreased = pyqtSignal(int)

    def __init__(self, parent):
        super(WorkerPD, self).__init__()
        self.parent = parent
        self._step = int(self.parent.stbord)
        self._isRunning = False
        self._maxSteps = 20

    def task(self):
        self.parent.btnStopPD.show()
        self.parent.btnStartPD.hide()
        if not self._isRunning:
            self._isRunning = True
            self._step = int(self.parent.stbord)

        while self._isRunning == True:
            if self._step == int(self.parent.labord):
                self._step = self.parent.stbord - 1
            self._step += 1
            self.stepIncreased.emit(self._step)
            time.sleep(-self.parent.SliderAU.value()/100)

        self._step = 0
        print("finished...")

    def stop(self):
        self.parent.btnStopPD.hide()
        self.parent.btnStartPD.show()
        self._step = 0
        self._isRunning = False

class WorkerUA(QObject):
    'Object managing the simulation'

    stepIncreased = pyqtSignal(int)

    def __init__(self, parent):
        super(WorkerUA, self).__init__()
        self.parent = parent
        self._step = int(self.parent.i)
        self._isRunning = False
        self._maxSteps = 20

    def task(self):
        self.parent.btnStopAU.show()
        self.parent.btnStartAU.hide()
        if not self._isRunning:
            self._isRunning = True
            self._step = int(self.parent.i)

        while self._isRunning == True:
            if self._step == len(self.parent.df['Event'].unique()) - 1:
                self._step = -1
            self._step += 1
            self.stepIncreased.emit(self._step)
            time.sleep(-self.parent.SliderAU.value()/100)

        self._step = 0
        print("finished...")

    def stop(self):
        self.parent.btnStopAU.hide()
        self.parent.btnStartAU.show()
        self._step = 0
        self._isRunning = False

def drowA(parent, st):
        sipm = []
        ch = []
        znach = []
        X = []
        Y = []

        o = parent.df[parent.df['Event'] == int(parent.event)]

        for i in parent.coords[parent.coords['SIPM'] == 1]['ch'].unique().tolist():
            sipm.append(1)
            ch.append(i)
            znach.append(max(o[(o['SIPM'] == 1) & (o['ch'] == i)].iloc[0, 5+st:5+st+1]))
        #print(o[(o['SIPM'] == 1) & (o['ch'] == i)].iloc[0, 4:1024])

        for i in parent.coords[parent.coords['SIPM'] == 2]['ch'].unique().tolist():
            sipm.append(2)
            ch.append(i)
            znach.append(max(o[(o['SIPM'] == 2) & (o['ch'] == i)].iloc[0, 5+st:5+st+1]))

        cmap = cm.get_cmap(parent.theme)

        znach.append(parent.nowAmax)

        norm = Normalize(vmin=min(znach), vmax=max(znach))
        rgba_values = cmap(norm(znach))
        znach.pop()

        for Si, c, col, z in zip(sipm, ch, rgba_values, znach):
            for i in parent.buttons:   
                if i.sipm == Si and i.ch == c:
                    i.rgbcol = col

                    #h, l, s = colorsys.rgb_to_hls(col[0], col[1], col[2])
                    #h = (h + 0.1) % 1
                    #s = 0.5
                    #l = 1
                    #i.textcol = matplotlib.colors.rgb2hex(colorsys.hls_to_rgb(h, s, l))

                    if (sum(col) - 1) / 3 < 0.5:
                        i.textcol = matplotlib.colors.rgb2hex((1, 1, 1))
                    else:
                        i.textcol = matplotlib.colors.rgb2hex((0, 0, 0))

                    #i.textcol = matplotlib.colors.rgb2hex((s - r, s - g, s - b))
                    i.col = matplotlib.colors.rgb2hex(col)
                    i.setStyleSheet("QPushButton {background-color: "+ i.col +" ; color: White;  border-radius: "+str(int(i.frameSize().width()/2))+"px; }"
                                        "QPushButton:pressed {background-color:#b784a7)} ;")         
                    i.znach = z
                    i.setText(f'{z}\nSIPM:{i.sipm}\nPin:{i.ch}')

                    break
        print(i)
        parent.newSize()

def drow(parent):
        sipm = []
        ch = []
        znach = []
        X = []
        Y = []

        o = parent.df[parent.df['Event'] == int(parent.event)]

        for i in parent.coords[parent.coords['SIPM'] == 1]['ch'].unique().tolist():
            sipm.append(1)
            ch.append(i)
            znach.append(max(o[(o['SIPM'] == 1) & (o['ch'] == i)].iloc[0, 5+parent.stbord:5+parent.labord]))
        #print(o[(o['SIPM'] == 1) & (o['ch'] == i)].iloc[0, 4:1024])

        for i in parent.coords[parent.coords['SIPM'] == 2]['ch'].unique().tolist():
            sipm.append(2)
            ch.append(i)
            znach.append(max(o[(o['SIPM'] == 2) & (o['ch'] == i)].iloc[0, 5+parent.stbord:5+parent.labord]))

        cmap = cm.get_cmap(parent.theme)

        norm = Normalize(vmin=min(znach), vmax=max(znach))
        rgba_values = cmap(norm(znach))

        for Si, c, col, z in zip(sipm, ch, rgba_values, znach):
            for i in parent.buttons:   
                if i.sipm == Si and i.ch == c:
                    i.rgbcol = col

                    #h, l, s = colorsys.rgb_to_hls(col[0], col[1], col[2])
                    #h = (h + 0.1) % 1
                    #s = 0.5
                    #l = 1
                    #i.textcol = matplotlib.colors.rgb2hex(colorsys.hls_to_rgb(h, s, l))

                    if (sum(col) - 1) / 3 < 0.5:
                        i.textcol = matplotlib.colors.rgb2hex((1, 1, 1))
                    else:
                        i.textcol = matplotlib.colors.rgb2hex((0, 0, 0))

                    #i.textcol = matplotlib.colors.rgb2hex((s - r, s - g, s - b))
                    i.col = matplotlib.colors.rgb2hex(col)
                    i.setStyleSheet("QPushButton {background-color: "+ i.col +" ; color: White;  border-radius: "+str(int(i.frameSize().width()/2))+"px; }"
                                        "QPushButton:pressed {background-color:#b784a7)} ;")         
                    i.znach = z
                    i.setText(f'{z}\nSIPM:{i.sipm}\nPin:{i.ch}')

                    break
        parent.nowAmax = max(znach)
        parent.newSize()

def Data(filename):
    columns = ['Event', 'SIPM', 'SIPMKadr', 'Time', 'ch'] + [f'{i}' for i in range(1024)]
    try:
        df = pd.read_csv(filename, sep="\s+", encoding="windows-1251", header=None, index_col=False, names=columns)
    except ValueError:
        return 0
    df = df.dropna()
    df['SIPM'] = df["SIPM"].astype(int)
    df['ch'] = df["ch"].astype(int)
    return df

class VisualWindow(QMainWindow):

    resized = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.setWindowTitle("Settings")
        self.setMinimumWidth(650)
        self.setMinimumHeight(400)
        self.setFixedSize(390, 200)

        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.resized.connect(self.newSize)
        
        self.sizeButtons = QDoubleSpinBox(self)
        self.sizeButtons.move(10, 5)
        self.sizeButtons.setValue(float(self.parent.settings.get('Set_SIMPS', 'buttonsHW')))
        self.sizeButtons.valueChanged.connect(self.changeSizeButtons)
        self.sizeButtons.setMinimum(0.1)
        self.sizeButtons.setFixedSize(60, 25)

        self.sizeButtonsT = QLabel('size of pixel', self)
        self.sizeButtonsT.setFixedSize(70, 25)
        self.sizeButtonsT.move(75, 5)

        self.spinX = QDoubleSpinBox(self)
        self.spinX.move(10, 30)
        self.spinX.setValue(float(self.parent.settings.get('Set_SIMPS', 'moveX'))) 
        self.spinX.valueChanged.connect(self.changeSpinX)
        self.spinX.setMinimum(0.1)
        self.spinX.setFixedSize(60, 25)

        self.spinXT = QLabel('distance between pixels by X', self)
        self.spinXT.setFixedSize(170, 25)
        self.spinXT.move(75, 30)

        self.spinY = QDoubleSpinBox(self)
        self.spinY.move(10, 55)
        self.spinY.setValue(float(self.parent.settings.get('Set_SIMPS', 'moveY'))) 
        self.spinY.valueChanged.connect(self.changeSpinY)
        self.spinY.setMinimum(0.1)
        self.spinY.setFixedSize(60, 25)

        self.spinYT = QLabel('distance between pixels by Y', self)
        self.spinYT.setFixedSize(170, 25)
        self.spinYT.move(75, 55)

        self.moveX = QSpinBox(self)
        self.moveX.move(10, 80)
        self.moveX.setMinimum(-10000)
        self.moveX.setValue(int(self.parent.settings.get('Set_SIMPS', 'movingX'))) 
        self.moveX.valueChanged.connect(self.changeMovingX)
        self.moveX.setFixedSize(60, 25)

        self.moveXT = QLabel('shift by X', self)
        self.moveXT.setFixedSize(170, 25)
        self.moveXT.move(75, 80)
        
        self.moveY = QSpinBox(self)
        self.moveY.move(10,105)
        self.moveY.setMinimum(-10000)
        self.moveY.setValue(int(self.parent.settings.get('Set_SIMPS', 'movingY'))) 
        self.moveY.valueChanged.connect(self.changeMovingY)
        self.moveY.setFixedSize(60, 25)

        self.moveYT = QLabel('shift by Y', self)
        self.moveYT.setFixedSize(170, 25)
        self.moveYT.move(75, 105)

        self.setDefultsettings = QPushButton('load defult settings', self)
        self.setDefultsettings.move(10, 160)
        self.setDefultsettings.setFixedSize(180, 30)
        self.setDefultsettings.clicked.connect(self.setDefultSETTINGS)
        
        self.saveSettingsInFILE = QPushButton('save settings in file', self)
        self.saveSettingsInFILE.move(200, 160)
        self.saveSettingsInFILE.setFixedSize(180, 30)
        self.saveSettingsInFILE.clicked.connect(self.saveSettingsInFile)

        self.HSznach = QCheckBox(self)
        self.HSznach.toggled.connect(self.HSZNACH)
        self.HSznach.setChecked(False if self.parent.settings.get('Set_HStext', 'HZnach') == '1' else True)
        #self.HSznach.setFixedSize(25, 25) 
        self.HSznach.move(250, 5)

        self.HSznachT = QLabel('hide A max', self)
        self.HSznachT.setFixedSize(170, 25)
        self.HSznachT.move(275, 5)

        self.HSsipm = QCheckBox(self)
        self.HSsipm.toggled.connect(self.HSSIPM)
        self.HSsipm.setChecked(False if self.parent.settings.get('Set_HStext', 'HSipm') == '1' else True) 
        self.HSsipm.move(250, 30)

        self.HSsipmT = QLabel('hide SIPM numbers', self)
        self.HSsipmT.setFixedSize(170, 25)
        self.HSsipmT.move(275, 30)

        self.HSchan = QCheckBox(self)
        self.HSchan.toggled.connect(self.HSCHAN)
        self.HSchan.setChecked(False if self.parent.settings.get('Set_HStext', 'HChan') == '1' else True) 
        self.HSchan.move(250, 55)

        self.HSchanT = QLabel('hide pixel numbers', self)
        self.HSchanT.setFixedSize(170, 25)
        self.HSchanT.move(275, 55)

        self.stb = QSpinBox(self)
        self.stb.setMinimum(0)
        self.stb.setMaximum(1023)
        self.stb.setValue(self.parent.stbord)
        self.stb.valueChanged.connect(self.changebord)
        self.stb.setFixedSize(60, 25)
        self.stb.move(100, 130)

        self.stbT = QLabel('find A-max from', self)
        self.stbT.move(10, 130)

        self.lab = QSpinBox(self)
        self.lab.setMinimum(0)
        self.lab.setMaximum(1023)
        self.lab.setValue(self.parent.labord)
        self.lab.valueChanged.connect(self.changebord)
        self.lab.setFixedSize(60, 25)
        self.lab.move(180, 130)

        self.labT = QLabel('to', self)
        self.labT.move(165, 130)
        self.labT.setFixedSize(25, 25)

        self.theme = QComboBox(self)
        self.theme.addItem(self.parent.settings.get('Set_theme', 'theme'))
        self.theme.addItems(['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Grays', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'crest', 'crest_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'flare', 'flare_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_grey', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gist_yerg', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'grey', 'hot', 'hot_r', 'hsv', 'hsv_r', 'icefire', 'icefire_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'mako', 'mako_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'rocket', 'rocket_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'vlag', 'vlag_r', 'winter', 'winter_r'])
        self.theme.activated.connect(self.changetheme)
        self.theme.setFixedSize(80, 25)
        self.theme.move(230, 85)

        self.themeT = QLabel(' - theme', self)
        self.themeT.move(310, 85)
        self.themeT.setFixedSize(50, 25)

    def changetheme(self):
        self.parent.theme = self.theme.currentText()
        self.parent.settings.set('Set_theme', 'theme', self.theme.currentText())
        self.parent.changetheme()

    def changebord(self):
        if self.stb.value() < self.lab.value():
            self.parent.stbord = self.stb.value()
            self.parent.labord = self.lab.value()
            self.parent.settings.set('Set_bord', 'st', f'{self.stb.value()}')
            self.parent.settings.set('Set_bord', 'la', f'{self.lab.value()}')
            self.parent.setEventAndDrow()

    def HSZNACH(self):
        if self.HSznach.isChecked():
            self.parent.HZnach = False
        else:
            self.parent.HZnach = True
        self.parent.settings.set('Set_HStext', 'HZnach', f'{"1" if self.parent.HZnach else "0"}')
        self.parent.newSize()

    def HSSIPM(self):
        if self.HSsipm.isChecked():
            self.parent.HSipm = False
        else:
            self.parent.HSipm = True
        self.parent.settings.set('Set_HStext', 'HSipm', f'{"1" if self.parent.HSipm else "0"}')
        self.parent.newSize()

    def HSCHAN(self):
        if self.HSchan.isChecked():
            self.parent.HChan = False
        else:
            self.parent.HChan = True
        self.parent.settings.set('Set_HStext', 'HChan', f'{"1" if self.parent.HChan else "0"}')
        self.parent.newSize()

    def changeSpinX(self):
        self.parent.settings.set('Set_SIMPS', 'moveX', f'{self.spinX.value()}')
        self.parent.newSize()
    
    def changeSpinY(self):
        self.parent.settings.set('Set_SIMPS', 'moveY', f'{self.spinY.value()}')
        self.parent.newSize()

    def changeSizeButtons(self):
        self.parent.settings.set('Set_SIMPS', 'buttonsHW', f'{self.sizeButtons.value()}')
        self.parent.newSize()

    def changeMovingX(self):
        self.parent.settings.set('Set_SIMPS', 'movingX', f'{self.moveX.value()}')
        self.parent.newSize()

    def changeMovingY(self):
        self.parent.settings.set('Set_SIMPS', 'movingY', f'{self.moveY.value()}')
        self.parent.newSize()

    def setDefultSETTINGS(self):
        self.parent.settings = self.parent.DefultSettings()
        self.sizeButtons.setValue(float(self.parent.settings.get('Set_SIMPS', 'buttonsHW')))
        self.spinX.setValue(float(self.parent.settings.get('Set_SIMPS', 'moveX'))) 
        self.spinY.setValue(float(self.parent.settings.get('Set_SIMPS', 'moveY')))
        self.moveX.setValue(int(self.parent.settings.get('Set_SIMPS', 'movingX'))) 
        self.moveY.setValue(int(self.parent.settings.get('Set_SIMPS', 'movingY'))) 
        self.HSznach.setChecked(False if self.parent.settings.get('Set_HStext', 'HZnach') == '1' else True)
        self.HSsipm.setChecked(False if self.parent.settings.get('Set_HStext', 'HSipm') == '1' else True) 
        self.HSchan.setChecked(False if self.parent.settings.get('Set_HStext', 'HChan') == '1' else True)
        self.stb.setValue(int(self.parent.settings.get('Set_bord', 'st')))
        self.lab.setValue(int(self.parent.settings.get('Set_bord', 'la')))
        self.theme.clear()
        self.theme.addItem(self.parent.settings.get('Set_theme', 'theme'))
        self.theme.addItems(['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Grays', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'crest', 'crest_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'flare', 'flare_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_grey', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gist_yerg', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'grey', 'hot', 'hot_r', 'hsv', 'hsv_r', 'icefire', 'icefire_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'mako', 'mako_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'rocket', 'rocket_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'vlag', 'vlag_r', 'winter', 'winter_r'])
        self.parent.theme = self.parent.settings.get('Set_theme', 'theme')
        self.parent.changetheme()
        self.parent.newSize()

    def saveSettingsInFile(self):
        self.parent.saveSettingsInFile()

    def closeEvent(self, event):
        print("User has clicked the red x on the main window")
        self.parent.vid = False
        event.accept()

    def resizeEvent(self, event):
        self.resized.emit()
        return super(VisualWindow, self).resizeEvent(event)
    
    def newSize(self):
        #self.drow.move(self.centralwidget.frameSize().width() // 2 - 50, 30)
        print(99)
        #self.events.move(self.centralwidget.frameSize().width() - 75, 10)

class App(QMainWindow):

    resized = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        global buttonsHW, moveX, moveY

        if os.path.exists('config.ini') is not True:
            print(9)
            config = self.DefultSettings()
            with open('config.ini', 'w') as config_file:
                config.write(config_file)

        
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.settings = config

        self.nowAmax = 0

        self.setWindowTitle("LOLITA")
        self.setMinimumWidth(650)
        self.setMinimumHeight(450)

        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.resized.connect(self.newSize)
        
        self.nowevent = QLabel("Event", self)
        self.nowevent.hide()

        self.nowfile = QLabel("File", self)
        self.nowfile.setFixedSize(500, 25)
        self.nowfile.hide()

        self.time = QLabel("Time", self)
        self.time.setFixedSize(150, 10)
        self.time.hide()

        self.events = QComboBox(self)
        self.events.move(10, 30)
        self.events.activated.connect(self.changeEventsfromcombobox)
        self.events.hide()

        #self.theme = QComboBox(self)
        #self.theme.addItem(self.settings.get('Set_theme', 'theme'))
        #self.theme.addItems(['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Grays', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'crest', 'crest_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'flare', 'flare_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_grey', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gist_yerg', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'grey', 'hot', 'hot_r', 'hsv', 'hsv_r', 'icefire', 'icefire_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'mako', 'mako_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'rocket', 'rocket_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'vlag', 'vlag_r', 'winter', 'winter_r'])
        #self.theme.activated.connect(self.changetheme)
        #self.theme.hide()

        self.theme = self.settings.get('Set_theme', 'theme')

        self.buttonleft = QPushButton('<-', self)
        self.buttonleft.clicked.connect(self.changeEventsfromLBut)
        self.buttonleft.setFixedSize(25, 25)
        self.buttonleft.hide()

        self.buttonright = QPushButton('->', self)
        self.buttonright.clicked.connect(self.changeEventsfromRBut)
        self.buttonright.setFixedSize(25, 25)
        self.buttonright.hide()

        #self.showText.toggled.connect(self.onClicked)
        self.vid = False

        self.hideWidg = QCheckBox(self)
        self.hideWidg.move(90, 120)
        self.hideWidg.toggled.connect(self.changeHide)
        self.hideWidg.hide()
        
        self.HZnach = True if self.settings.get('Set_HStext', 'HZnach') == '1' else False
        self.HSipm = True if self.settings.get('Set_HStext', 'HSipm') == '1' else False
        self.HChan = True if self.settings.get('Set_HStext', 'HChan') == '1' else False

        self.stbord = int(self.settings.get('Set_bord', 'st'))
        self.labord = int(self.settings.get('Set_bord', 'la'))

        self.intervalT = QLabel("interval", self)
        self.intervalT.hide()

        self._createMenuBar()

        self.AllpInEvent = QPushButton('All pixels in event', self)
        self.AllpInEvent.move(50, 100)
        self.AllpInEvent.clicked.connect(self.AllPixelInEvent)
        self.AllpInEvent.hide()

        self.openASmatplot = QPushButton('event in plt\nwindow', self)
        self.openASmatplot.move(100, 100)
        self.openASmatplot.clicked.connect(self.openEventInMAatplot)
        self.openASmatplot.setFixedSize(100, 35)
        self.openASmatplot.hide()

        self.event = ''
        self.i = 0

        #

        self.btnStartAU = QPushButton('>', self)
        self.btnStartAU.move(90, 270)
        self.btnStartAU.setFixedSize(25, 25)
        self.btnStartAU.hide()
        #self.btnStartAU.hide()
        self.btnStopAU = QPushButton('||', self)
        self.btnStopAU.move(90, 270)
        self.btnStopAU.setFixedSize(25, 25)
        self.btnStopAU.hide()
        self.currentStepAU = QSpinBox(self)
        self.currentStepAU.move(30, 270)
        self.currentStepAU.hide()
    
        self.threadAU = QThread()
        self.threadAU.start()

        self.workerAU = WorkerUA(self)
        self.workerAU.moveToThread(self.threadAU)
        self.workerAU.stepIncreased.connect(self.currentStepAU.setValue)

        self.btnStopAU.clicked.connect(lambda: self.workerAU.stop())
        self.btnStartAU.clicked.connect(self.workerAU.task)
        

        self.currentStepAU.valueChanged.connect(self.AU)


        self.SliderAU = QSlider(self)
        self.SliderAU.setOrientation(Qt.Orientation.Horizontal) 
        self.SliderAU.setGeometry(30, 40, 100, 25)
        self.SliderAU.move(50, 50)
        self.SliderAU.setMinimum(-200)
        self.SliderAU.setMaximum(-10)
        self.SliderAU.hide()
        #SliderAU.valueChanged[int].connect(self.changeValue)

        self.btnStartPD = QPushButton('>', self)
        self.btnStartPD.move(60, 270)
        self.btnStartPD.setFixedSize(25, 25)
        self.btnStartPD.hide()
        #self.btnStartAU.hide()
        self.btnStopPD = QPushButton('||', self)
        self.btnStopPD.move(60, 270)
        self.btnStopPD.setFixedSize(25, 25)
        self.btnStopPD.hide()
        self.currentStepPD = QSpinBox(self)
        self.currentStepPD.setMinimum(0)
        self.currentStepPD.setMaximum(1025)
        self.currentStepPD.move(10, 270)
        self.currentStepPD.setFixedSize(50, 25)
        self.currentStepPD.hide()
    
        self.threadPD = QThread()
        self.threadPD.start()

        self.workerPD = WorkerPD(self)
        self.workerPD.moveToThread(self.threadPD)
        self.workerPD.stepIncreased.connect(self.currentStepPD.setValue)

        self.btnStopPD.clicked.connect(lambda: self.workerPD.stop())
        self.btnStartPD.clicked.connect(self.workerPD.task)
        

        self.currentStepPD.valueChanged.connect(self.PD)

        #self.finished.connect(self.stop_thread)
        
        self.newRegim = QPushButton("Change Mode", self)
        self.newRegim.move(40, 40)
        self.newRegim.hide()
        self.newRegim.clicked.connect(self.openNewRegim)

        self.isopenNewRegim = False

        self.buttons = []
        coords = pd.read_csv('dat.dat', sep='\s+')
        print(coords.head())
        #self.theme.addItems(['magma', 'Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Grays', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'crest', 'crest_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'flare', 'flare_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_grey', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gist_yerg', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'grey', 'hot', 'hot_r', 'hsv', 'hsv_r', 'icefire', 'icefire_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'mako', 'mako_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'rocket', 'rocket_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'vlag', 'vlag_r', 'winter', 'winter_r'])
        for sipm, x, y, ch in zip(coords['SIPM'], coords['x_sm'], coords['y_sm'], coords['ch']):
            but = QPushButton(f'{ch}', self)
            but.sipm = sipm
            but.x = x
            but.y = -y
            but.ch = ch
            but.f = False
            but.move(int(x*10), int(y*10))
            but.textcol = 'White'
            but.znach = None
            but.clicked.connect(self.openAdditWin)
            but.win = []
            if but.sipm == 2:
                but.col = '#1f75fe'
            else:
                but.col = '#c35831'
            self.buttons.append(but)
        self.coords = coords

        self.i = -1

    def openNewRegim(self):
        if self.workerAU._isRunning:
            print('Cantt')
        elif self.workerPD._isRunning:
            print(9)
        elif self.isopenNewRegim:
            print(9)
            self.isopenNewRegim = False
            #self.showNug()
            self.btnStopPD.hide()
            self.btnStartPD.hide()
            self.btnStartAU.show()
            self.btnStopAU.hide()
            self.currentStepPD.hide()
        else:
            print(10)
            self.isopenNewRegim = True
            self.btnStartAU.hide()
            self.btnStopAU.hide()
            self.btnStartPD.show()
            self.btnStopPD.hide()
            self.currentStepPD.show()
            #self.hideNug()
        print(self.isopenNewRegim)

    def PD(self):
        drowA(self, self.currentStepPD.value())
        print(self.currentStepPD.value())
        
    def AU(self):
        self.i = self.currentStepAU.value()
        self.event = self.AllItems[self.i]
        self.nowevent.setText(f"Event {self.event}")
        self.events.setCurrentText(self.event)
        self.nowtime = self.df[self.df['Event'] == int(self.event)]['Time'].unique()[0]
        self.time.setText(f'Time {self.nowtime}')
        self.intervalT.setText(f'interval {self.stbord} - {self.labord}')
        drow(self)

    def AllPixelInEvent(self):
        plot_data = self.df[self.df['Event'] == int(self.event)]
        x = range(0,1024)
        fig, ax = plt.subplots()
        for i in self.df['ch'].unique():
            y = plot_data[(plot_data['ch'] == i)&(plot_data['SIPM'] == 1)].iloc[0][5:]
            plt.plot(x, y, label=f"{str(i)} 1")
            y = plot_data[(plot_data['ch'] == i)&(plot_data['SIPM'] == 2)].iloc[0][5:]
            plt.plot(x, y, label=f"{str(i)} 2")
        ax.grid(linestyle='--', color='pink') 
        ax.set_xlim([0, 1023])
        ax.set_xlabel('time')
        ax.set_ylabel('amplitude')
        ax.set_title(f'All pixels in Event {self.event}')
        ax.legend(ncol=1, loc="upper left", bbox_to_anchor=(1,1))
        #plt.clf()
        plt.show()

    def openEventInMAatplot(self):
        print(100)
        sipm = []
        ch = []
        znach = []
        X = []
        Y = []

        for i in self.coords[self.coords['SIPM'] == 1]['ch'].tolist():
            sipm.append(1)
            ch.append(i)
            znach.append(max(self.df[(self.df['SIPM'] == 1) & (self.df['ch'] == i) & (self.df['Event'] == int(self.event))].iloc[0, 5+self.stbord:5+self.labord]))
    #print(o[(o['SIPM'] == 1) & (o['ch'] == i)].iloc[0, 4:1024])
            X.append(self.coords[(self.coords['SIPM'] == 1) & (self.coords['ch'] == int(i))]['x_sm'].unique().tolist()[0])
            Y.append(self.coords[(self.coords['SIPM'] == 1) & (self.coords['ch'] == int(i))]['y_sm'].unique().tolist()[0])


        for i in self.coords[self.coords['SIPM'] == 2]['ch'].tolist():
            sipm.append(2)
            ch.append(i)
            znach.append(max(self.df[(self.df['SIPM'] == 2) & (self.df['ch'] == i) & (self.df['Event'] == int(self.event))].iloc[0, 5+self.stbord:5+self.labord]))
            X.append(self.coords[(self.coords['SIPM'] == 2) & (self.coords['ch'] == int(i))]['x_sm'].unique().tolist()[0])
            Y.append(self.coords[(self.coords['SIPM'] == 2) & (self.coords['ch'] == int(i))]['y_sm'].unique().tolist()[0])
    
        cmap = cm.get_cmap(self.theme)
        fig, ax = plt.subplots(1, 1)

# нормализация данных
        norm = Normalize(vmin=min(znach), vmax=max(znach))
        rgba_values = cmap(norm(znach))

# координаты

        ax.set_aspect('equal')
        print(len(sipm), len(Y), len(Y), len(ch) ,len(rgba_values))
        for Si, x, y, c, col, z in zip(sipm, X, Y, ch, rgba_values, znach):
            hex = RegularPolygon((x, y), numVertices=6, radius=1.65, 
                orientation=np.radians(30), 
                facecolor=col, alpha=0.9, edgecolor=(0, 0, 0))
            ax.add_patch(hex)
            ax.text(x, y, f"{z}", ha ='center',
            va ='center', size = 10, color='red')

        ax.scatter(-15, -15, alpha=0.0)
        #ax.get_xaxis().set_visible(False)
        #ax.get_yaxis().set_visible(False)
        plt.subplots_adjust(left=0, bottom=0, right=1, top=0.9)
        plt.axis('off')

        #rect = Rectangle((-3.5,-14), height=1, width=3, ec="none", facecolor=(0.9, 0.5, 0.3), edgecolor=(0, 0, 0))
        #ax.add_patch(rect)
        #rect = Rectangle((0.5,-14), height=1, width=3, ec="none", facecolor=(0.3, 0.5, 0.9), edgecolor=(0, 0, 0))
        #ax.add_patch(rect)

        #ax.text(-2, -13.5, f"SIPM 1", ha ='center',
        #    va ='center', size = 10, color='black')
        #ax.text(2, -13.5, f"SIPM 2", ha ='center',
        #    va ='center', size = 10, color='black')

        plt.show()

    def changeHide(self):
        if self.hideWidg.isChecked():
            self.hideWidgets()
        else:
            self.showWidgets()

    def saveSettingsInFile(self):
        with open('config.ini', 'w') as config_file:
            self.settings.write(config_file)

    def openAdditWin(self):
        if self.event == "":
            return None
        
        b = self.sender()
        print(b.f)
        if not b.f:
            b.win.append(Chan(b, self))
            b.win[-1].show()
            b.f = True

    def DefultSettings(self):
        config = configparser.ConfigParser()
        config.add_section('Settings')
        config.set('Settings', 'username', 'user')
        config.set('Settings', 'password', 'pass')
        config.add_section('Set_SIMPS')
        config.set('Set_SIMPS', 'buttonsHW', '9.5')
        config.set('Set_SIMPS', 'moveX', '2.88')
        config.set('Set_SIMPS', 'moveY', '2.88')
        config.set('Set_SIMPS', 'movingX', '0')
        config.set('Set_SIMPS', 'movingY', '-20')
        config.add_section('Set_theme')
        config.set('Set_theme', 'theme', 'Blues')
        config.add_section('Set_HStext')
        config.set('Set_HStext', 'HZnach', '1')
        config.set('Set_HStext', 'HSipm', '1')
        config.set('Set_HStext', 'HChan', '1')
        config.add_section('Set_bord')
        config.set('Set_bord', 'st', '200')
        config.set('Set_bord', 'la', '250')

        return config

    def changetheme(self):
        if self.event != "":
            drow(self)

    def SavePng(self):
        if self.event != "":

            dialog = QFileDialog()
            for btn in dialog.findChildren(QPushButton):
                print(btn.text())
                print(888)
                if btn.text() == "Открыть":
                    btn.setText("Remove")
            print(000)
            dialog.setNameFilter('Text File (*.txt)')
            dialogSuccess = dialog.exec()



            if dialogSuccess:
                fileLocation = dialog.selectedFiles()[0]
                print(fileLocation)
        else: 
            QMessageBox.about(self, "Error", "Open file to save event")

    def OpenF(self):
        fname = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        
        if fname[0] != '':
            self.openingFile(fname[0])
        else:
            return None
        
    def openingFile(self, name):
        self.df = Data(name)

        if type(self.df) == int:
            QMessageBox.about(self, "Error", "Error at the file opening stage")
            return None
        
        if self.df.empty :
            QMessageBox.about(self, "Error", "The data file is empty")
            return None

        self.hideWidg.show()
        self.btnStartAU.show()
        self.SliderAU.show()
        #self.btnStartPD.show()
        #self.currentStepPD.show()
        self.showWidgets()
        self.addItemsToEvents()
        s = 0
        for i in range(len(name)):
            if name[i] == "/":
                s = i
        print('-----', s)
        self.nowfile.setText(f"File Name {name[s+1:]}")
        self.AllItems = [self.events.itemText(i) for i in range(self.events.count())]
        self.i = self.events.currentIndex()
        self.changeEventsfromcombobox()

    def addItemsToEvents(self):
        self.events.clear()
        self.events.addItems([str(i) for i in self.df['Event'].unique()])

    def hideNug(self):
        self.buttonright.hide()
        self.buttonleft.hide()
        self.btnStartAU.hide()
        self.btnStopAU.hide()
        self.SliderAU.hide()

    def showNug(self):
        self.buttonright.show()
        self.buttonleft.show()
        self.btnStartAU.show()
        self.btnStopAU.show()
        self.SliderAU.show()

    def hideWidgets(self):
        self.newRegim.hide()
        self.openASmatplot.hide()
        self.AllpInEvent.hide()
        self.intervalT.hide()
        self.time.hide()
        self.nowevent.hide()
        self.nowfile.hide()
        self.events.hide()
        self.events.hide()
        self.buttonleft.hide()
        self.buttonright.hide()


    def showWidgets(self):
        self.newRegim.show()
        self.openASmatplot.show()
        self.AllpInEvent.show()
        self.intervalT.show()
        self.time.show()
        self.nowevent.show()
        self.nowfile.show()
        self.events.show()
        self.events.show()
        self.buttonleft.show()
        self.buttonright.show()

    def changeEventsfromLBut(self):
        if self.i == 0:
            self.i = len(self.AllItems)
        self.i = self.i - 1
        self.workerAU._step = int(self.i)
        self.setEventAndDrow()

    def changeEventsfromRBut(self):
        if self.i == len(self.AllItems) - 1:
            self.i = -1
        self.i += 1
        self.workerAU._step = int(self.i)
        self.setEventAndDrow()

    def changeEventsfromcombobox(self):
        self.event = self.events.currentText()
        self.i = self.events.currentIndex()
        self.nowevent.setText(f"Event {self.event}")
        print(self.event)
        print(self.i)
        self.setEventAndDrow()
        
    def setEventAndDrow(self):
        print(self.df.head())
        self.event = self.AllItems[self.i]
        self.nowevent.setText(f"Event {self.event}")
        self.events.setCurrentText(self.event)
        self.nowtime = self.df[self.df['Event'] == int(self.event)]['Time'].unique()[0]
        self.time.setText(f'Time {self.nowtime}')
        self.intervalT.setText(f'interval {self.stbord} - {self.labord}')
        print(self.i)
        drow(self)

    def _createMenuBar(self):
        menuBar = self.menuBar()

        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        self.openFile = QAction("&Open...", self)
        #self.saveasPng = QAction("&Save as PNG", self)

        self.openFile.triggered.connect(self.OpenF)
        #self.saveasPng.triggered.connect(self.SavePng)

        fileMenu.addAction(self.openFile)
        #fileMenu.addAction(self.saveasPng)

        editMenu = menuBar.addMenu("&Settings")
        self.setVisual = QAction("&SetVisual...", self)
        self.setVisual.triggered.connect(self.openVisualwin)
        editMenu.addAction(self.setVisual)

        helpMenu = menuBar.addMenu("&Help")

    def newSize(self):
        buttonsHW = float(self.settings.get('Set_SIMPS', 'buttonsHW'))
        moveX = float(self.settings.get('Set_SIMPS', 'moveX'))
        moveY = float(self.settings.get('Set_SIMPS', 'moveY'))
        movingX = int(self.settings.get('Set_SIMPS', 'movingX'))
        movingY = int(self.settings.get('Set_SIMPS', 'movingY'))

        H = self.centralwidget.frameSize().height()
        W = self.centralwidget.frameSize().width()

        #self.theme.move(W - 110, 30)
        self.nowevent.move(10, H - 30)
        self.nowfile.move(10, H - 10)
        self.time.move(10, H - 40)

        self.intervalT.move(10, H - 70)

        self.hideWidg.move(10, H - 90)

        self.buttonleft.move(W // 2 - 10 - 25, H - 10)
        self.buttonright.move(W // 2 + 10, H - 10)

        self.AllpInEvent.move(W - 110, H - 10)
        self.openASmatplot.move(W - 110, H - 45)

        self.btnStartAU.move(W - 140, H - 70)
        self.btnStopAU.move(W - 140, H - 70)
        self.SliderAU.move(W - 110, H - 70)

        self.newRegim.move(W - 220, H - 10)

        self.btnStartPD.move(W - 170, H - 70)
        self.btnStopPD.move(W - 170, H - 70)
        self.currentStepPD.move(W - 220, H - 70)

        S = min(round(H/buttonsHW), round(W/buttonsHW))
        w = round(W/2)
        h = round(H/2)
        for i in self.buttons:
            i.setFixedSize(S, S)
            
            i.setStyleSheet(" QPushButton {background-color: " + i.col + " ; color: " + i.textcol +" ; border-radius: "+str(int(i.frameSize().width()/2))+"px; font-size: " +str(int(i.frameSize().width()/4.3))+ "px ;} " # QPushButton:hover { background-color: rgb(16, 16, 24) ; color: rgb(76, 76, 76);}
                                        "QPushButton:pressed {background-color: #b784a7 ; }")
            if i.znach is None:
                i.setText(f'{i.ch}')   
            else:
                if self.HZnach and self.HChan and not self.HSipm:
                    i.setText(f'{int(i.znach)}\nCh:{i.ch}') 
                else:
                    k = str(str(int(i.znach)) + str("\n" if self.HSipm else "") if self.HZnach else "") + str("SIPM:" + str(i.sipm) + str("\n" if self.HChan else "") if self.HSipm else "") + str("Ch:" + str(i.ch) if self.HChan else "")
                    i.setText(k)   
            i.move(round(i.x * S / moveX + w)-S//2+movingX, round(i.y * S / moveY + h)+movingY)
            

    def openVisualwin(self):
        if not self.vid:
            self.vid = True
            self.win = VisualWindow(self)
            self.win.show()

    def closeEvent(self, event):
        for i in self.buttons:
            for j in i.win:
                j.close()
        if self.vid:
            self.win.close()

    def resizeEvent(self, event):
        self.resized.emit()
        return super(App, self).resizeEvent(event)
    
class Chan(QMainWindow):

    resized = QtCore.pyqtSignal()
    
    def __init__(self, b, parent):
        
        super().__init__()
        self.setGeometry(300, 50, 230, 100)
        self.setMinimumWidth(230)
        self.setMinimumHeight(100)
        self.setWindowTitle(f"S{b.sipm} C{b.ch} ")

        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.resized.connect(self.newSize)

        self.parent = parent


        self.chan = QLabel(f"Chan: {b.ch}", self)
        self.chan.move(10, 10)

        self.sipm = QLabel(f"SIPM: {b.sipm}", self)
        self.sipm.move(10, 30)

        self.amax  = QLabel(f"A Max: {b.znach}", self)
        self.amax.move(10, 50)

        self.event = QComboBox(self)
        self.event.clear()
        self.event.addItems(['All'] + [str(i) for i in parent.df['Event'].unique()])
        self.event.setFixedSize(40, 25)
        self.event.move(230, 10)
        self.event.activated.connect(self.drowew)

        self.drownowevent = QPushButton(f'Draw now\nevent ({self.parent.event})', self)
        self.drownowevent.setFixedSize(65, 40)
        self.drownowevent.clicked.connect(self.drowNowEvent)

        self.Or = QLabel('or', self)
        self.Or.move(20, 20)
        self.Or.setFixedSize(25, 25)

        self.time = QLabel(f'Time: {self.parent.nowtime}', self)
        self.time.move(10, 70)

        self.b = b

    def drowew(self):
        if self.event.currentText() == "All":
            plot_data = self.parent.df[(self.parent.df['ch'] == self.b.ch) & (self.parent.df['SIPM'] == self.b.sipm)]
            x = range(0,1024)
            fig, ax = plt.subplots()
            for i in self.parent.df['Event'].unique():
                y = plot_data[plot_data['Event'] == i].iloc[0][5:]
                plt.plot(x, y, label=f"{str(i)}")
            ax.grid(linestyle='--', color='pink') 
            ax.set_xlim([0, 1023])
            ax.set_xlabel('time')
            ax.set_ylabel('amplitude')
            ax.set_title(f'S{self.b.sipm} C{self.b.ch} In All Events')
            ax.legend(ncol=1, loc="upper left", bbox_to_anchor=(1,1))
            #plt.clf()
            plt.show()
            
        else:
            plot_data = self.parent.df[((self.parent.df['Event'] == int(self.event.currentText()))&(self.parent.df['ch'] == self.b.ch)&(self.parent.df['SIPM'] == self.b.sipm))]
            print(plot_data.head())
            y = plot_data.iloc[0][5:].tolist()
            x = range(0,1024)
            fig, ax = plt.subplots()
            #ax.figure(figsize=(7,4))
            ax.plot(x, y)
            ax.set_title(f'Event {self.event.currentText()} S{self.b.sipm} C{self.b.ch}')
            ax.grid(linestyle='--', color='pink')
            ax.set_xlim([0, 1023])
            ax.set_xlabel('time')
            ax.set_ylabel('amplitude')
            #plt.clf()
            plt.show()


    def drowNowEvent(self):
        print(self.b.ch)
        print(self.b.sipm)
        plot_data = self.parent.df[((self.parent.df['Event'] == int(self.parent.event))&(self.parent.df['ch'] == self.b.ch)&(self.parent.df['SIPM'] == self.b.sipm))]
        print(plot_data.head())
        y = plot_data.iloc[0][5:].tolist()
        x = range(0,1024)
        plt.figure(figsize=(7,4))
        plt.plot(x, y)
        plt.title(f'Event {self.parent.event} Time: {self.parent.nowtime} S{self.b.sipm} C{self.b.ch}')
        ax = plt.gca()
        ax.set_xlim([0, 1023])
        ax.set_xlabel('time')
        ax.set_ylabel('amplitude')
        #ax.set_ylim([, ])
        plt.grid(linestyle='--', color='pink') 
        plt.savefig('0.png', bbox_inches='tight')
        plt.show()
        #plt.clf()

    def resizeEvent(self, event):
        self.resized.emit()
        return super(Chan, self).resizeEvent(event)
    
    def closeEvent(self, event):
        self.b.f = False
    
    def newSize(self):
        #self.drow.move(self.centralwidget.frameSize().width() // 2 - 50, 30)
        self.drownowevent.move(self.centralwidget.frameSize().width() // 2 - 50, 10)
        self.event.move(self.centralwidget.frameSize().width() - 50, 10)
        self.Or.move(self.centralwidget.frameSize().width() // 4 * 3 - 22, 10)
        #self.events.move(self.centralwidget.frameSize().width() - 75, 10)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())