# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
import sys
import sqlite3
from ana_sayfa import *
from Kitap_Ekle import *
from KitapEkleDialog import KitapEkleDialog

class AnaSayfa(QDialog):
    def __init__(self):
        super().__init__()
        self.ui=Ui_Anasayfa()
        self.ui.setupUi(self)
        self.currow=0
        
        self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)

        
        #tıklama sinyali
        self.ui.btnEkle.clicked.connect(self.Ekle_sayfasi)
        self.ui.btnDuzenle.clicked.connect(self.Duzenle_sayfasi)
        self.ui.btnSil.clicked.connect(self.sil_kitap)
        self.ui.leKitapara.textChanged.connect(self.ARA)
        self.ui.btnsonraki.clicked.connect(self.SONRAKI)
        self.ui.btnonceki.clicked.connect(self.ONCEKI)
        
        self.ui.tableWidget.itemSelectionChanged.connect(self.itemSelectionChanged)
        
        
        #Database İşlemi
        self.conn=sqlite3.connect("kutuphane.db") #veri tabanı varsa açar ve yoksa oluşturur
        self.curs=self.conn.cursor()  ##sql komutlarını kullanmak execute etmek için cursor
        
        ##
        self.kitaplari_listele()
        
        
    def kitaplari_listele(self,sql="SELECT * FROM kitaplar"):
        self.ui.tableWidget.setRowCount(0)
        self.curs.execute(sql)
        kitaplar = self.curs.fetchall()
        
        rowcount=len(kitaplar) #kayıt sayısı elde ediliyor
    
        # Her kitap için tabloya satır ekle
        for satir_numarasi, kitap in enumerate(kitaplar):
            self.ui.tableWidget.insertRow(satir_numarasi)
    
            for sutun_numarasi, veri in enumerate(kitap):
                item = QTableWidgetItem(str(veri))
                self.ui.tableWidget.setItem(satir_numarasi, sutun_numarasi, item)
        # currow sınır kontrolü
        if rowcount == 0:
            self.currow = 0
        elif self.currow >= rowcount:
            self.currow = rowcount - 1
        elif self.currow < 0:
            self.currow = 0
    
        self.ui.tableWidget.setCurrentCell(self.currow, 0)
        self.ui.progressBar.setMaximum(max(rowcount, 1))  # max 0 olmasın
        self.ui.progressBar.setValue(self.currow + 1)
    
    
    def itemSelectionChanged(self):
        indeks = self.ui.tableWidget.currentIndex()
        self.currow = indeks.row()
        self.ui.progressBar.setValue(self.currow + 1)
        

    def Ekle_sayfasi(self):
        sayfa=KitapEkleDialog()
        sayfa.exec_()
        self.kitaplari_listele()
        
    def Duzenle_sayfasi(self):
        secilen_satir = self.ui.tableWidget.currentRow()
        if secilen_satir < 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen düzenlemek istediğiniz kitabı seçin!")
            return
    
        kitap = []
        for i in range(5):  # id, ad, yazar, tür, basimyili
            kitap.append(self.ui.tableWidget.item(secilen_satir, i).text())
    
        sayfa = KitapEkleDialog(kitap)  
        sayfa.exec_()
        self.kitaplari_listele()

        
    def sil_kitap(self):
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
        
    def ARA(self):
        sql="SELECT * FROM kitaplar WHERE ad LIKE'%"+self.ui.leKitapara.text()+"%'"
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
           
    
            

        

        
        
    


if (__name__=="__main__"):
    app=QApplication(sys.argv) ##application oluşturuluyor
    window=AnaSayfa()
    window.show()
    sys.exit(app.exec_()) #pencereden çıkarken uygulama ile lgili tüm işlemler sonlandırılıyor