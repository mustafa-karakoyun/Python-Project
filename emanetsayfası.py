# -*- coding: utf-8 -*-
"""
Created on Fri May 30 18:57:34 2025

@author: karak
"""

from PyQt5.QtWidgets import *
import sys
import sqlite3
from emanet import *


class Emanet(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Emanet()
        self.ui.setupUi(self)
        
        
        
        #Database İşlemi
        self.conn=sqlite3.connect("kutuphane.db") #veri tabanı varsa açar ve yoksa oluşturur
        self.curs=self.conn.cursor()  ##sql komutlarını kullanmak execute etmek için cursor
        
        #SİGNAL SLOTLAR
        
        self.ui.btniptal.clicked.connect(self.iptal)
        self.ui.btnKaydet.clicked.connect(self.kaydet)
        
        
        #Tamamlayıcı kitap ismi girldikçe onerileri cıkıyor
        kitap_adlari = self.kitaplari_getir()
        tamamlayici = QCompleter(kitap_adlari)
        tamamlayici.setCaseSensitivity(False)  # Büyük/küçük harfe duyarsız
        self.ui.leSecim.setCompleter(tamamlayici)
        
    def kitaplari_getir(self):
        self.curs.execute("SELECT ad FROM kitaplar")
        kitaplar = [row[0] for row in self.curs.fetchall()]
        return kitaplar
        
    def kaydet(self):
        uye=self.ui.leUyeAd.text()
        kitap = self.ui.leSecim.text()
        verilis = self.ui.dateVerilis.date().toString("dd-MM-yyyy")
        teslim = self.ui.dateTeslim.date().toString("dd-MM-yyyy")
        
        if uye == "" or kitap == "":
            QMessageBox.warning(self, "Uyarı", "Üye adı ve kitap adı boş bırakılamaz.")
            return

        # Id bulunuyor
        self.curs.execute("SELECT id FROM kitaplar WHERE ad = ?", (kitap,))
        sonuc = self.curs.fetchone()
    
        if sonuc is None:
            QMessageBox.warning(self, "Hata", "Girilen kitap bulunamadı.")
            return
    
        kitap_id = sonuc[0]
    
        # Veritabanı eklentisi
        self.curs.execute("""
            INSERT INTO emanet (uyeadi, kitapid, verilmetarihi, teslimtarihi)
            VALUES (?, ?, ?, ?)
        """, (uye, kitap_id, verilis, teslim))
        self.conn.commit()
    
        QMessageBox.information(self, "Başarılı", "Emanet kaydedildi.")
        self.YENI()
        
    def YENI(self):
        self.ui.leUyeAd.setText("")
        self.ui.leSecim.setText("")
        self.ui.dateTeslim.clear()
        self.ui.dateVerilis.clear()
        
        
        self.ui.leSecim.setFocus(True) 
        
    def iptal(self):
        self.close()
        
        

if (__name__=="__main__"):
    app=QApplication(sys.argv) ##application oluşturuluyor
    window=Emanet()
    window.show()
    sys.exit(app.exec_()) #pencereden çıkarken uygulama ile lgili tüm işlemler sonlandırılıyor