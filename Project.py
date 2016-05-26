#!/usr/bin/python3
#-*-coding:utf-8-*-

import sys
import os
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from GUI import Ui_MainWindow
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import (QPixmap)
from PyQt5.QtWidgets import (QFileDialog, QGraphicsScene)

class GUI(Ui_MainWindow):
    def __init__(self):
        super().setupUi(MainWindow)
        self.initUI()
    def initUI(self):
        self.actionOpen.triggered.connect(self.imageOpen)
    def imageOpen(self):
#        filename,_ = QFileDialog.getOpenFileName(MainWindow,'Open a image',os.getenv('HOME'))
#        filename,_ = QFileDialog.getOpenFileName(MainWindow,'Open a image','.',"Image Files(*.bmp *jpg *png)")
        filename="/home/lab105/git-sen/python_gui/lena512.bmp"
#        print(filename)
        image=QtGui.QPixmap(filename)
        image=image.scaledToHeight(256)
        scene=QGraphicsScene()
        scene.addPixmap(QPixmap(image))
        self.graphicsView.setScene(scene)

if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)
    MainWindow=QtWidgets.QMainWindow()
    ui=GUI()
    MainWindow.show() 
    sys.exit(app.exec_())
