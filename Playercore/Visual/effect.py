from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import random as rnd
import time as tm
import math as ma
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
        self.quit()

class FlashFuncFast(QThread):
    FlashOPint=pyqtSignal(float,int)
    def __init__(self):
        super(FlashFuncFast,self).__init__()

    def run(self):
        self.FlashOPint.emit(0,0)
        for i in range(0,20):
            a=round(ma.sin(i*0.157),2)
            self.FlashOPint.emit(a,1)
            tm.sleep(0.02)
        self.FlashOPint.emit(0,2)
        self.quit()

class FlashFuncSlow(QThread):
    FlashOPint=pyqtSignal(float,int)
    def __init__(self):
        super(FlashFuncSlow,self).__init__()

    def run(self):
        self.FlashOPint.emit(0,0)
        for i in range(0,40):
            a=round(ma.sin(i*0.0785),2)
            self.FlashOPint.emit(a,1)
            tm.sleep(0.02)
        self.FlashOPint.emit(0,2)
        self.quit()
