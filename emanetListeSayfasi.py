# -*- coding: utf-8 -*-
"""
Created on Fri May 30 19:45:52 2025

@author: karak
"""

from PyQt5.QtWidgets import *
import sys
import sqlite3
from emanetListeui import *

class EmanetList(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_EmanetListe()
        self.ui.setupUi(self)
        self.currow=0
        
        #Tüm satırı seçme
        self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        
        #Database İşlemi
        self.conn=sqlite3.connect("kutuphane.db") #veri tabanı varsa açar ve yoksa oluşturur
        self.curs=self.conn.cursor()  ##sql komutlarını kullanmak execute etmek için cursor
        
        self.ui.tableWidget.itemSelectionChanged.connect(self.itemSelectionChanged)
        
        
        self.ui.btnYukari_2.clicked.connect(self.SONRAKI)
        self.ui.btnYukari.clicked.connect(self.ONCEKI)
        
        self.kitaplari_listele()
        
    def itemSelectionChanged(self):
        indeks = self.ui.tableWidget.currentIndex()
        self.currow = indeks.row()
        self.ui.progressBar.setValue(self.currow + 1)
        
    def kitaplari_listele(self, sql="SELECT * FROM emanet"):
        self.ui.tableWidget.setRowCount(0)
        self.curs.execute(sql)
        emanetler = self.curs.fetchall()
        
        self.ui.progressBar.setMaximum(len(emanetler))

    
        for satir_numarasi, emanet in enumerate(emanetler):
            self.ui.tableWidget.insertRow(satir_numarasi)
    
            for sutun_numarasi, veri in enumerate(emanet):
                item = QTableWidgetItem(str(veri))
                self.ui.tableWidget.setItem(satir_numarasi, sutun_numarasi, item)
        
        if hasattr(self, 'currow') and 0 <= self.currow < len(emanetler):
            self.ui.tableWidget.setCurrentCell(self.currow, 0)
        else:
            self.ui.tableWidget.setCurrentCell(0, 0)
            
    
    def SONRAKI(self):
        self.currow+=1
        if (self.currow==self.ui.tableWidget.rowCount()):
            self.currow=0
        self.ui.tableWidget.setCurrentCell(self.currow,0)
    
    def ONCEKI(self):
        self.currow-=1
        if (self.currow<0):
            self.currow=self.ui.tableWidget.rowCount()-1
        self.ui.tableWidget.setCurrentCell(self.currow,0)

        
if (__name__=="__main__"):
    app=QApplication(sys.argv) ##application oluşturuluyor
    window=EmanetList()
    window.show()
    sys.exit(app.exec_()) #pencereden çıkarken uygulama ile lgili tüm işlemler sonlandırılıyor

