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
from skimage.filter import (threshold_otsu, rank)
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
        self.GrayvalueScrollBar.valueChanged.connect(self.sliderval)
        self.OTSU.clicked.connect(self.OTSUThreshold)

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
        n,self.bins,patches=plt.hist(x,num_bins,normed=1,facecolor='green',alpha=0.5)
        plt.axis("off")
        plt.gca().set_position([0,0,1,1])
        self.figure=plt.gcf()
        canvas2=FigureCanvas(self.figure)
        scene2=QGraphicsScene()
        scene2.addWidget(canvas2)
        self.View2.setScene(scene2)


    def sliderval(self):
        Threshold=self.GrayvalueScrollBar.value()
        self.Binarization(Threshold)
#        self.label.setText(str(Threshold))

    #threshlod function 
    def Binarization(self,Threshold):
        #filename="/home/lab105/git-sen/python_gui/lena512.bmp"
        #img=misc.imread(filename)
        img=self.image
        BinaryArray=np.where(img>=Threshold,0,1)
        plt.figure(figsize=(256,256),dpi=1)
        plt.axis("off")
        plt.gca().set_position([0,0,1,1]) 
        plt.imshow(BinaryArray,cmap='binary')
        figure3=plt.gcf()
        canvas3=FigureCanvas(figure3)
        plt.close(figure3)
        scene3=QGraphicsScene()
        scene3.addWidget(canvas3)
        self.View4.setScene(scene3)
        self.label.setText(str(Threshold))

    def OTSUThreshold(self):
        img=self.image
        thresh=threshold_otsu(img)
        binary=img < thresh

        plt.figure(figsize=(256,256),dpi=1)
        plt.axis("off")
        plt.gca().set_position([0,0,1,1])
        plt.imshow(binary,cmap='binary')
        figure4=plt.gcf()
        canvas4=FigureCanvas(figure4)
        plt.close(figure4)
        scene4=QGraphicsScene()
        scene4.addWidget(canvas4)
        self.View3.setScene(scene4)

if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)
    MainWindow=QtWidgets.QMainWindow()
    ui=GUI()
    MainWindow.show() 
    sys.exit(app.exec_())
