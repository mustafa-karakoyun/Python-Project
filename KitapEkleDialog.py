# -*- coding: utf-8 -*-
"""
Created on Thu May 29 20:27:30 2025

@author: karak
"""

from PyQt5.QtWidgets import *
import sys
import sqlite3

from ana_sayfa import *
from Kitap_Ekle import *

from PyQt5.QtWidgets import QDialog
from Kitap_Ekle import Ui_KitapEkleDialog  # senin otomatik oluşturulan UI dosyan

class KitapEkleDialog(QDialog):
    def __init__(self, kitap=None):  # kitap=None -> ekleme, doluysa -> düzenleme
        super().__init__()
        self.ui = Ui_KitapEkleDialog()
        self.ui.setupUi(self)
        self.currow=0
        
        self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        
        
        #Database İşlemi
        self.conn=sqlite3.connect("kutuphane.db") #veri tabanı varsa açar ve yoksa oluşturur
        self.curs=self.conn.cursor()  ##sql komutlarını kullanmak execute etmek için cursor
        
        self.kitaplari_listele()
        

        self.kitap = kitap
        #ıd nin değişmemesi için
        self.ui.leid.setReadOnly(True) 
        self.ui.leid.setEnabled(False) 

        if self.kitap:
            self.setWindowTitle("Kitap Düzenle")
            self.ui.leid.setText(kitap[0])
            self.ui.leid.setEnabled(False)       

            self.ui.leKitapAdi.setText(self.kitap[1])
            self.ui.leYazar.setText(self.kitap[2])
            self.ui.leYazar_2.setText(self.kitap[4])
            #self.ui.comboBox.setText(self.kitap[4])
        else:
            self.setWindowTitle("Yeni Kitap Ekle")
        
        ###BUTON BAGLANTILARI
        self.ui.btnDuzelt.clicked.connect(self.Duzelt)
        self.ui.btnekle.clicked.connect(self.Ekle)
        self.ui.btnSil.clicked.connect(self.Sil)
        self.ui.btnYeni.clicked.connect(self.YENI)
        self.ui.btnCikis.clicked.connect(self.Cikis)
        self.ui.lineEdit.textChanged.connect(self.ARA)
        self.ui.btnAsagi.clicked.connect(self.SONRAKI)
        self.ui.btnYukari.clicked.connect(self.ONCEKI)
        
        self.ui.tableWidget.itemSelectionChanged.connect(self.itemSelectionChanged)
        
        
        
    def kitaplari_listele(self,sql="SELECT * FROM kitaplar"):
        
        self.ui.tableWidget.setRowCount(0)
        conn = sqlite3.connect("kutuphane.db")
        curs = conn.cursor()
        self.curs.execute(sql)
        kitaplar = self.curs.fetchall()
    
        # Her kitap için tabloya satır ekle
        for satir_numarasi, kitap in enumerate(kitaplar):
            self.ui.tableWidget.insertRow(satir_numarasi)
    
            for sutun_numarasi, veri in enumerate(kitap):
                item = QTableWidgetItem(str(veri))
                self.ui.tableWidget.setItem(satir_numarasi, sutun_numarasi, item)
                
        self.ui.tableWidget.setCurrentCell(self.currow,0) #setCurrentCell(curentrow,curentcell)
        #KİTAP EKLEME İŞLEMİ İÇİN
    def Ekle(self):
       
        ad = self.ui.leKitapAdi.text()
        yazar = self.ui.leYazar.text()
        tur = self.ui.comboBox.currentText() 
        yil = self.ui.leYazar_2.text()        
        conn = sqlite3.connect("kutuphane.db")
        curs = conn.cursor()
        curs.execute("INSERT INTO kitaplar (ad, yazar, tür, basımyılı) VALUES (?, ?, ?, ?)",
                     (ad, yazar, tur, yil))
        QMessageBox.information(self, "Başarılı", "Kitap Eklendi")
        conn.commit()
        conn.close()
        
        self.currow = self.ui.tableWidget.rowCount()  # son satır
        self.kitaplari_listele()
        
        
        #DÜZELTME BUTONU
    def Duzelt(self):
        ad = self.ui.leKitapAdi.text()
        yazar = self.ui.leYazar.text()
        tur = self.ui.comboBox.currentText()  # tür ComboBox'tan alınıyor
        yil = self.ui.leYazar_2.text()         # yıl alanı örnek
        conn = sqlite3.connect("kutuphane.db")
        curs = conn.cursor()
        curs.execute("UPDATE kitaplar SET ad=?, yazar=?, tür=?, basımyılı=? WHERE id=?",
                     (ad, yazar, tur, yil, self.kitap[0]))
        QMessageBox.information(self, "Başarılı","Kitap güncellendi")

        conn.commit()
        conn.close()
        self.accept()
    
    def Sil(self):
       response=QMessageBox().question(self,"Silme Onay","Seçili kaydı silmek istediğinize emin misin?",QMessageBox().Yes| QMessageBox().No)
       if response==QMessageBox().Yes:
           selectedrow=self.ui.tableWidget.selectedItems()
           silinecek=selectedrow[0].text()
           sql="DELETE FROM kitaplar WHERE id=?"
           parameter=[silinecek]
           self.curs.execute(sql,parameter)
           self.conn.commit()
           QMessageBox().information(self,"Bilgilendirme","Kaydınız Silindi")
           self.kitaplari_listele()
         
    def YENI(self):
        self.ui.leKitapAdi.setText("")
        self.ui.leYazar.setText("")
        self.ui.leYazar_2.setText("")
        
        self.ui.leKitapAdi.setFocus(True) #True derseniz en başa konumlanır. False en sona
        
    def Cikis(self):
        soru = QMessageBox.question(self, "Çıkış", "Çıkış yapmak istiyor musunuz?", QMessageBox.Yes | QMessageBox.No)
        if soru == QMessageBox.Yes:
            self.close()
            
    def ARA(self):
        sql = "SELECT * FROM kitaplar WHERE ad LIKE '%{}%' OR yazar LIKE '%{}%'".format(self.ui.lineEdit.text(), self.ui.lineEdit.text())
        self.kitaplari_listele(sql)
        
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
        
            
    def TabletoForm(self):
            selectedrows = self.ui.tableWidget.selectedItems()
            if selectedrows and len(selectedrows) >= 5:
                self.kitap = [item.text() for item in selectedrows[:5]]
                self.ui.leid.setText(self.kitap[0])
                self.ui.leKitapAdi.setText(self.kitap[1])
                self.ui.leYazar.setText(self.kitap[2])
                self.ui.comboBox.setCurrentText(self.kitap[3])
                self.ui.leYazar_2.setText(self.kitap[4])

            
    def itemSelectionChanged(self):
        indeks=self.ui.tableWidget.currentIndex()  #PyQt5.QtCore.QModelIndex türünde nesne döndürür
        self.currow=indeks.row() #bu nesnenin row() metodu ile satır index'i elde ediliyor
        self.TabletoForm()
            

            
        
            
        
    
       
            
    
        
           

if (__name__=="__main__"):
    app=QApplication(sys.argv) ##application oluşturuluyor
    window=KitapEkleDialog()
    window.show()
    sys.exit(app.exec_()) #pencereden çıkarken uygulama ile lgili tüm işlemler sonlandırılıyor