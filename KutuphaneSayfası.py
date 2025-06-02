# -*- coding: utf-8 -*-
"""
Created on Sat May 31 17:22:21 2025

@author: karak
"""

from PyQt5.QtWidgets import *
import sys
import sqlite3
from Kutuphaneui import *
from AnaSayfa import *
from KitapEkleDialog import *
from emanetsayfası import *
from emanetListeSayfasi import *

from PyQt5.QtGui import QPixmap


class Kutuphane(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.pushButton.clicked.connect(self.Kitaplar)
        self.ui.pushButton_2.clicked.connect(self.islem)
        self.ui.pushButton_3.clicked.connect(self.Emanet)
        self.ui.pushButton_4.clicked.connect(self.EmanetListesi)
        
        #görsel
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap("arka.jpg"))
        self.label.setScaledContents(True)
        self.label.resize(self.size())
        self.label.lower()

        # Diğer arayüz elemanlarını buraya ekleyebilirsin

    def resizeEvent(self, event):
        self.label.resize(self.size())
        return super().resizeEvent(event)
    
    
    def Kitaplar(self):
        sayfa=AnaSayfa()
        sayfa.exec_()
        
    def islem(self):
        sayfa=KitapEkleDialog()
        sayfa.exec_()

    def Emanet(self):
        sayfa=Emanet()
        sayfa.exec_()    
        
    def EmanetListesi(self):
        sayfa=EmanetList()
        sayfa.exec_()
        
        
    
    
if (__name__=="__main__"):
    app=QApplication(sys.argv) ##application oluşturuluyor
    window=Kutuphane()
    window.show()
    sys.exit(app.exec_()) #pencereden çıkarken uygulama ile lgili tüm işlemler sonlandırılıyor