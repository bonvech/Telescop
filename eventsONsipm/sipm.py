import sys
import pandas as pd
import os

from matplotlib.colors import Normalize
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon, Rectangle
import seaborn as sns


from PyQt6 import uic  # Импортируем uic
from PyQt6.QtWidgets import QApplication, QDialog, QFileDialog
from PyQt6.QtGui import QPixmap

class Drowka():
    def drow(self):

        sipm = []
        ch = []
        znach = []
        X = []
        Y = []
        kadr = Data.kadr
        if kadr == '':
            return None
        o = Data.File[Data.File['Kadr'] == int(kadr)]
        q = Data.q

        for i in q[q['SIPM'] == 1]['ch'].unique().tolist():
            sipm.append(1)
            ch.append(i)
            znach.append(max(o[(o['SIPM'] == 1) & (o['ch'] == i)].iloc[0, 229:230]))
        #print(o[(o['SIPM'] == 1) & (o['ch'] == i)].iloc[0, 4:1024])
            X.append(q[(q['SIPM'] == 1) & (q['ch'] == int(i))]['x_sm'].unique().tolist()[0])
            Y.append(q[(q['SIPM'] == 1) & (q['ch'] == int(i))]['y_sm'].unique().tolist()[0])


        for i in q[q['SIPM'] == 2]['ch'].unique().tolist():
            sipm.append(2)
            ch.append(i)
            znach.append(max(o[(o['SIPM'] == 2) & (o['ch'] == i)].iloc[0, 100:1000]))
            X.append(q[(q['SIPM'] == int(2)) & (q['ch'] == int(i))]['x_sm'].unique().tolist()[0])
            Y.append(q[(q['SIPM'] == int(2)) & (q['ch'] == int(i))]['y_sm'].unique().tolist()[0])

        print(sipm, ch, znach)

        cmap = cm.get_cmap('magma')
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))

        norm = Normalize(vmin=min(znach), vmax=max(znach))
        rgba_values = cmap(norm(znach))

    # координаты
        for Si, x, y, c, col, z in zip(sipm, X, Y, ch, rgba_values, znach):
            hex = RegularPolygon((x, y), numVertices=6, radius=1.65, 
                orientation=np.radians(30), 
                facecolor=col, alpha=0.9, edgecolor=(0, 0, 0))
            ax.add_patch(hex)
            ax.text(x, y, f"{z:.0f}", ha ='center', va ='center', size = 10, color='red')

        ax.scatter(-10, -10, alpha=0.0)
        ax.set_aspect('equal')
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        rect = Rectangle((-3.5,-14), height=1, width=3, ec="none", facecolor=(0.9, 0.5, 0.3), edgecolor=(0, 0, 0))
    #ax.add_patch(rect)
        rect = Rectangle((0.5,-14), height=1, width=3, ec="none", facecolor=(0.3, 0.5, 0.9), edgecolor=(0, 0, 0))
    #ax.add_patch(rect)

    #ax.text(-2, -13.5, f"SIPM 1", ha ='center', va ='center', size = 10, color='black')
    #ax.text(2, -13.5, f"SIPM 2", ha ='center',  va ='center', size = 10, color='black')
        plt.subplots_adjust(left=0, bottom=0, right=1, top=0.800)
        plt.axis('off')
        fig.savefig(f'0.png')
        plt.clf()
        self.load_image('0.png')

class Data():
    File = pd.DataFrame()
    q = pd.DataFrame()
    kadr = ''
    kadrs = []
    
    def __init__(self, filename):
        columns = ['Kadr', 'SIPM', 'SIPMKadr', 'Time', 'ch'] + [f'{i}' for i in range(1024)]
        df = pd.read_csv(filename, sep="\s+", encoding="windows-1251", header=None, index_col=False, names=columns)
        df = df.dropna()
        df['SIPM'] = df["SIPM"].astype(int)
        df['ch'] = df["ch"].astype(int)
        Data.File = df

        q = pd.read_csv('xy.dat', sep='\s+')

        Sipm = q['SIPM'].to_list()
        x_sm = q['x_sm'].to_list()
        y_sm = q['y_sm'].to_list()
        

        Data.q = q


class MyWidget(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('vigual2.ui', self)  # Загружаем дизайн
        self.load_file.clicked.connect(self.lf)
        self.postr.clicked.connect(self.droww)
        self.leftB.clicked.connect(self.left)
        self.rightB.clicked.connect(self.right)
        # Обратите внимание: имя элемента такое же как в QTDesigner

    def lf(self):
        fname = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        
        if fname[0] != '':
            Data(fname[0])
        else:
            return None
        
        
        self.kadrs.clear()
        self.kadrs.addItems([str(i) for i in Data.File['Kadr'].unique()])
        Data.kadrs = [str(i) for i in Data.File['Kadr'].unique()]
        Data.kadr = self.kadrs.currentText()

    def left(self):
        if Data.kadr == "":
            return None
        e = Data.kadrs.index(Data.kadr)
        if e == len(Data.kadrs) - 1:
            Data.kadr = Data.kadrs[0]
            self.nowkadr.setText(f"Кадар {Data.kadr}")
            Drowka.drow(self)
            return None
        Data.kadr = Data.kadrs[e + 1]
        self.nowkadr.setText(f"Кадар {Data.kadr}")
        Drowka.drow(self)

    def right(self):
        if Data.kadr == "":
            return None
        e = Data.kadrs.index(Data.kadr)
        if e == 0:
            self.nowkadr.setText(f"Кадар {Data.kadr}")
            Drowka.drow(self)
            Data.kadr = Data.kadrs[-1]   
        Data.kadr = Data.kadrs[e - 1]
        self.nowkadr.setText(f"Кадар {Data.kadr}")
        Drowka.drow(self) 

    def droww(self):
        Data.kadr = self.kadrs.currentText()
        self.nowkadr.setText(f"Кадар {Data.kadr}")
        Drowka.drow(self)
        
    def load_image(self, file_name):
        pixmap = QPixmap(file_name)
        self.label.setPixmap(pixmap)
        self.label.resize(pixmap.width(), pixmap.height())
        self.label.move(300, 2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
