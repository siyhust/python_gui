#!/usr/bin/python3
#-*-coding:utf-8-*-

import pdb
import sys
import os
from scipy import (ndimage, misc)
import numpy as np
#import matplotlib.mlab as mlab
#import matplotlib
#matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from skimage.filter import (threshold_otsu)
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
        self.scene1=QGraphicsScene()
        self.scene2=QGraphicsScene()
        self.scene3=QGraphicsScene()
        self.scene4=QGraphicsScene()
        self.actionOpen.triggered.connect(self.imageOpen)
        self.histogram.clicked.connect(self.imageHistogram)
        self.GrayvalueScrollBar.valueChanged.connect(self.sliderval)
        self.OTSU.clicked.connect(self.OTSUThreshold)
        self.MedianFilter.clicked.connect(self.medianfilter)
        self.MeanFilter.clicked.connect(self.meanfilter)
        self.GaussianFilter.clicked.connect(self.gaussianfilter)
        self.CoustomizedFilter.clicked.connect(self.coustomizefilter)
        self.BinaryErosion.clicked.connect(self.binaryerosion)
        self.BinaryDilation.clicked.connect(self.binarydilation)
        self.actionClear_All.triggered.connect(self.clearall)
        self.DistanceTransform.clicked.connect(self.distancetransform)

    #function menubar-file-open: Open image and show it in view1
    def imageOpen(self):
#        filename,_ = QFileDialog.getOpenFileName(MainWindow,'Open a image',os.getenv('HOME'))
        filename,_ = QFileDialog.getOpenFileName(MainWindow,'Open a image','.',"Image Files(*.bmp *jpg *png *jpeg)")
#        filename="/home/lab105/git-sen/python_gui/lena512.bmp"
#        print(filename)
        pix=QtGui.QPixmap(filename)
        pix=pix.scaledToHeight(256)
        self.image=plt.imread(filename)
        Size=self.image.shape
        if (len(Size)==3):
            if (type(self.image[1,1,1]) is np.float32):
                self.image=misc.imread(filename) 
            self.image=self.image[:,:,1]
        self.image_temp=self.image
        self.scene1.addPixmap(QPixmap(pix))
        self.View1.setScene(self.scene1)

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
        self.scene2.addWidget(canvas2)
        self.View2.setScene(self.scene2)


    def sliderval(self):
        Threshold=self.GrayvalueScrollBar.value()
        self.Binarization(Threshold)
#        self.label.setText(str(Threshold))

    #threshlod function 
    def Binarization(self,Threshold):
        #filename="/home/lab105/git-sen/python_gui/lena512.bmp"
        #img=misc.imread(filename)
        img=self.image
        BinaryArray= img >Threshold
        plt.close(3)
        plt.figure(num=3,figsize=(256,256),dpi=1)
        plt.axis("off")
        plt.gca().set_position([0,0,1,1]) 
        plt.imshow(BinaryArray,cmap='binary_r')
        figure3=plt.gcf()
        canvas3=FigureCanvas(figure3)
        self.scene3.clear()
        self.scene3.addWidget(canvas3)
        self.View3.setScene(self.scene3)
        self.label.setText(str(Threshold))

    def OTSUThreshold(self):
        img=self.image
        thresh=threshold_otsu(img)
        binary=img > thresh
        self.showView4(binary)

    def showView4(self,image):
        plt.close(4)
        plt.figure(num=4,figsize=(256,256),dpi=1)
        if (image.max()>1):
            plt.imshow(image,cmap='gray')
        else:
            plt.imshow(image,cmap='binary_r')
        plt.gca().set_position([0,0,1,1])
        plt.axis("off")
        figure4=plt.gcf()
        canvas4=FigureCanvas(figure4)
        self.scene4.clear()
        self.scene4.addWidget(canvas4)
        self.View4.setScene(self.scene4)

    def getmatrixsize(self):
        matrixsize=3
        if (self.radioButton_1.isChecked()):
            matrixsize=3
        if (self.radioButton_2.isChecked()):
            matrixsize=5
        return matrixsize
    
    def medianfilter(self):
        self.image_temp=ndimage.median_filter(self.image_temp,size=int(self.plainTextEdit.toPlainText()))
        self.showView4(self.image_temp)

    def meanfilter(self):
        self.image_temp=ndimage.uniform_filter(self.image_temp,size=int(self.plainTextEdit.toPlainText()))
        self.showView4(self.image_temp)

    def gaussianfilter(self):
        self.image_temp=ndimage.gaussian_filter(self.image_temp,sigma=float(self.plainTextEdit_2.toPlainText()))
        self.showView4(self.image_temp)
    
    def getmatrix(self):
        self.Matrix=[]
        if (self.getmatrixsize()==3):
            matrix=np.zeros((3,3))
            matrix[0,0]=float(self.plainTextEdit1_1.toPlainText())
            matrix[0,1]=float(self.plainTextEdit1_2.toPlainText())
            matrix[0,2]=float(self.plainTextEdit1_3.toPlainText())
            matrix[1,0]=float(self.plainTextEdit2_1.toPlainText())
            matrix[1,1]=float(self.plainTextEdit2_2.toPlainText())
            matrix[1,2]=float(self.plainTextEdit2_3.toPlainText())
            matrix[2,0]=float(self.plainTextEdit3_1.toPlainText())
            matrix[2,1]=float(self.plainTextEdit3_2.toPlainText())
            matrix[2,2]=float(self.plainTextEdit3_3.toPlainText())
        if (self.getmatrixsize()==5):
            matrix=np.zeros((5,5))
            matrix[0,0]=float(self.plainTextEdit1_1.toPlainText())
            matrix[0,1]=float(self.plainTextEdit1_2.toPlainText())
            matrix[0,2]=float(self.plainTextEdit1_3.toPlainText())
            matrix[0,3]=float(self.plainTextEdit1_4.toPlainText())
            matrix[0,4]=float(self.plainTextEdit1_5.toPlainText())
            matrix[1,0]=float(self.plainTextEdit2_1.toPlainText())
            matrix[1,1]=float(self.plainTextEdit2_2.toPlainText())
            matrix[1,2]=float(self.plainTextEdit2_3.toPlainText())
            matrix[1,3]=float(self.plainTextEdit2_4.toPlainText())
            matrix[1,4]=float(self.plainTextEdit2_5.toPlainText())
            matrix[2,0]=float(self.plainTextEdit3_1.toPlainText())
            matrix[2,1]=float(self.plainTextEdit3_2.toPlainText())
            matrix[2,2]=float(self.plainTextEdit3_3.toPlainText())
            matrix[2,3]=float(self.plainTextEdit3_4.toPlainText())
            matrix[2,4]=float(self.plainTextEdit3_5.toPlainText())
            matrix[3,0]=float(self.plainTextEdit4_1.toPlainText())
            matrix[3,1]=float(self.plainTextEdit4_2.toPlainText())
            matrix[3,2]=float(self.plainTextEdit4_3.toPlainText())
            matrix[3,3]=float(self.plainTextEdit4_4.toPlainText())
            matrix[3,4]=float(self.plainTextEdit4_5.toPlainText())
            matrix[4,0]=float(self.plainTextEdit5_1.toPlainText())
            matrix[4,1]=float(self.plainTextEdit5_2.toPlainText())
            matrix[4,2]=float(self.plainTextEdit5_3.toPlainText())
            matrix[4,3]=float(self.plainTextEdit5_4.toPlainText())
            matrix[4,4]=float(self.plainTextEdit5_5.toPlainText())
        self.Matrix=matrix

    def coustomizefilter(self):
        self.getmatrix()
        self.image_temp=ndimage.correlate(self.image_temp,self.Matrix)
        self.showView4(self.image_temp)

    def binaryerosion(self):
        self.getmatrix()
        self.image_temp=ndimage.binary_erosion(self.image_temp,self.Matrix)
        self.showView4(self.image_temp)

    def binarydilation(self):
        self.getmatrix()
        self.image_temp=ndimage.binary_dilation(self.image_temp,self.Matrix)
        self.showView4(self.image_temp)

    def distancetransform(self):
        Size=self.image_temp.shape
        distance=np.zeros(Size)
        distance=distance+self.image_temp
        self.getmatrix()
        while (self.image_temp.max()!=0):
            self.image_temp=ndimage.binary_erosion(self.image_temp,self.Matrix)
            distance=distance+self.image_temp
        self.showView4(distance)

    def clearall(self):
        self.scene2.clear()
        self.scene3.clear()
        self.scene4.clear()
        self.image_temp=self.image

if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)
    MainWindow=QtWidgets.QMainWindow()
    ui=GUI()
    MainWindow.show() 
    sys.exit(app.exec_())
