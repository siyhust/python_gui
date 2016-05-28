#!/usr/bin/python3
#-*-coding:utf-8-*-

import sys
import os
from scipy import (ndimage, misc)
import numpy as np
#import matplotlib.mlab as mlab
#import matplotlib
#matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from GUI import Ui_MainWindow
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import (QPixmap, QImage)
from PyQt5.QtWidgets import (QFileDialog, QGraphicsScene)

class GUI(Ui_MainWindow):
    def __init__(self):
        super().setupUi(MainWindow)
        self.initUI()
    #connect widgets with functions
    def initUI(self):
        self.actionOpen.triggered.connect(self.imageOpen)
        self.histogram.clicked.connect(self.imageHistogram)


    #function menubar-file-open: Open image and show it in view1
    def imageOpen(self):
#        filename,_ = QFileDialog.getOpenFileName(MainWindow,'Open a image',os.getenv('HOME'))
#        filename,_ = QFileDialog.getOpenFileName(MainWindow,'Open a image','.',"Image Files(*.bmp *jpg *png *jpeg)")
        filename="/home/lab105/git-sen/python_gui/lena512.bmp"
#        print(filename)
        pix=QtGui.QPixmap(filename)
        pix=pix.scaledToHeight(256)
        self.image=misc.imread(filename)
        scene1=QGraphicsScene()
        scene1.addPixmap(QPixmap(pix))
        self.View1.setScene(scene1)

    #function mainwindow tab histogram-greylevel histogram: compute and show the greyvalue histogram in view 2
    def imageHistogram(self):
        greyimage=self.image
        #greyimage.dtype
        Height, Width=greyimage.shape
        x=np.zeros(Height*Width)
        for h in range(Height):
            for w in range(Width):
                x[h*Height+w]=greyimage[h,w]

        num_bins=255
        plt.figure(figsize=(256,256),dpi=1)
        plt.hist(x,num_bins,normed=1,facecolor='green',alpha=0.5)
        plt.axis("off")
        plt.gca().set_position([0,0,1,1])
        self.figure=plt.gcf()

        canvas=FigureCanvas(self.figure)
        scene2=QGraphicsScene()
        scene2.addWidget(canvas)
        self.View2.setScene(scene2)


if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)
    MainWindow=QtWidgets.QMainWindow()
    ui=GUI()
    MainWindow.show() 
    sys.exit(app.exec_())
