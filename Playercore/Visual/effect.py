from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import random as rnd
import time as tm

class Function():
    def __init__(self):
        None
    def Mapcolorfade(self,QIMAGE_O):
        X=QIMAGE_O.width()
        Y=QIMAGE_O.height()
        QIMAGE_N=QImage(X,Y,QImage.Format_ARGB32)
        oldcolor=QColor()
        for x in range(0,X):
            for y in range(0,Y):
                oldcolor=QColor(QIMAGE_O.pixel(x,y))
                r=oldcolor.red()+70
                g=oldcolor.green()+30
                b=oldcolor.blue()-10
                if r>255:r=255
                if g>255:g=255
                if b<0:b=0
                QIMAGE_N.setPixel(x,y,qRgb(r,g,b))
        return QIMAGE_N

    def Mapcolordark(self,QIMAGE_O):
        X=QIMAGE_O.width()
        Y=QIMAGE_O.height()

        QIMAGE_N=QImage(X,Y,QImage.Format_ARGB32)
        oldcolor=QColor()
        for x in range(0,X):
            for y in range(0,Y):
                oldcolor=QColor(QIMAGE_O.pixel(x,y))
                r=oldcolor.red()-50
                g=oldcolor.green()-50
                b=oldcolor.blue()-50
                a=oldcolor.alpha()
                if r<0:r=0
                if g<0:g=0
                if b<0:b=0
                QIMAGE_N.setPixel(x,y,qRgba(r,g,b,a))
        return QIMAGE_N

class ShakeFunc(QThread):
    shakeXY=pyqtSignal(int,int,int)
    def __init__(self):
        super(ShakeFunc,self).__init__()

    def run(self):
        for i in range(0,10):
            a=rnd.randint(-10,10)
            b=rnd.randint(-10,10)
            self.shakeXY.emit(a,b,0)
            tm.sleep(0.02)
        self.shakeXY.emit(0,0,1)