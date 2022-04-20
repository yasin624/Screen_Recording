import os

from PyQt5.QtWidgets import QWidget,QMainWindow,QSlider,QCheckBox,QLabel,QPushButton,QLineEdit,QApplication,QVBoxLayout,QHBoxLayout,QStatusBar,QComboBox
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtCore import QTimer,QTime,QThread,QSize,Qt
import cv2,sys,numpy,PyQt5
import matplotlib.pyplot as plt
from PIL import ImageGrab
from threading import Thread
from mss import mss

sct=mss()
"""
for i in dir(sct):
    print(i)
print("#"*100)
print("#"*100)
print("#"*100)

for i in dir(sct.monitorenumproc.errcheck):
    print(i)
print(str(sct.monitorenumproc))
print("#"*100)"""
class kaydet(QWidget):
    def __init__(self):
        super().__init__()
        ############################################## pencere ozeliklewri
        self.setWindowTitle("video kaydet  VS_20.10.21")
        self.setWindowIcon(QIcon("logo.ico"))
        self.setGeometry(0,0,500,140)
        self.basla()
        self.a=0
        self.b=0
        self.c=0
        self.video_name="sunum_denemesi"
    def zaman_say(self):
        say=str(self.a)+":"+str(self.b)+":"+str(self.c)
        self.zaman.setText(say)
        self.c+=1
        if self.c==60:
            self.c=0
            self.b+=1
        if self.b==60:
            self.c=0
            self.b=0
            self.a+=1

    def basla(self):
        ######################################  saat  yazılması
        self.zaman = QLabel(self)
        self.zaman.setText("0:0:0")
        self.zaman.setFont(QFont("Bold", 25))

        ################################### saat nesnesi olusturma
        self.saat=QTimer()

        ###############################################   baslat ,durdur ve selfi butonları
        self.buton=QPushButton(self)
        self.buton.setIcon(QIcon("basla.png"))
        self.buton.setText("kayıt")
        self.buton.setFont(QFont("Ariel",10))

        self.buton2 = QPushButton(self)
        self.buton2.setText("Durdur")
        self.buton2.setFont(QFont("Ariel", 10))
        self.buton2.blockSignals(True)

        ##########################################   selfi için
        self.selfi = QSlider(Qt.Horizontal)
        self.selfi.setMaximum(1)
        self.selfi.setMinimum(0)
        self.selfi.setSingleStep(1)
        selfi = Thread(target=self.wepcam)
        selfi.start()

        self.selfi2 = QPushButton(self)
        self.selfi2.setIcon(QIcon(" "))
        self.selfi2.blockSignals(True)

        self.selfi1 = QPushButton(self)
        self.selfi1.setIcon(QIcon("selfi0.jpg"))
        self.selfi1.blockSignals(True)



        self.buton2.setIcon(QIcon(""))

        self.buton.clicked.connect(self.bak)

        #####################################################  cozunurluk ayarları
        # ac kapat setEnabled

        self.cozünürlük=QComboBox()

        ##################################################### coklu ekran varsa
        if len(sct.monitors)>2:
            self.monitor = QComboBox()
            for i in range(len(sct.monitors)):
                if str(sct.monitors[i]["width"])+" x "+str(sct.monitors[i]["height"])!="1920 x 1080":
                    self.cozünürlük.addItem(str(sct.monitors[i]["width"])+" x "+str(sct.monitors[i]["height"]))

            for i in range(len(sct.monitors)):
                self.monitor.addItem("{} ekran".format(i))

            self.monitor.setEditable(True)
        ####################################################  çözünürlükler
        self.cozünürlük.addItem("1920 x 1080")
        self.cozünürlük.addItem("1640 x 1080")
        self.cozünürlük.addItem("1280 x 720")
        self.cozünürlük.addItem("853 x 480")
        self.cozünürlük.addItem("640 x 360")

        self.cozünürlük.setEditable(True)

        #####################################################   iceriklerin sabitlemeleri
        v = QHBoxLayout()
        v.addStretch()
        v.addWidget(self.buton)
        v.addWidget(self.buton2)
        v.addStretch()
        v.addStretch()


        alt = QHBoxLayout()
        alt.addWidget(self.selfi1)
        alt.addWidget(self.selfi)
        alt.addWidget(self.selfi2)
        alt.addStretch()
        alt.addWidget(self.cozünürlük)
        if len(sct.monitors) > 2:
            alt.addWidget(self.monitor)
        alt.addStretch()


        zaman = QVBoxLayout()
        zaman.addStretch()
        zaman.addWidget(self.zaman)
        zaman.addStretch()

        h = QVBoxLayout()
        h.addLayout(alt)
        h.addStretch()
        h.addLayout(v)
        h.addStretch()
        h.addWidget(QLabel("<h4>   Tüm hakları saklıdır © 2020 | yalcınyazılımcılık </h4>"))

        birles=QHBoxLayout()
        birles.addLayout(h)
        birles.addStretch()
        birles.addLayout(zaman)
        birles.addStretch()
        self.setLayout(birles)
    def wepcam(self):
        while True:
            if self.selfi.value()==1:
                self.selfi1.setIcon(QIcon(" "))
                self.selfi2.setIcon(QIcon("selfi3.png"))
                self.profile()

    def profile(self):

        self.wepcam = cv2.VideoCapture(0)
        dur=True
        while True:
            if cv2.waitKey(25) & self.selfi.value() == 0:
                self.wepcam.release()
                cv2.destroyAllWindows()
                self.selfi1.setIcon(QIcon("selfi0.jpg"))
                self.selfi2.setIcon(QIcon(" "))
                break

            _, img = self.wepcam.read()
            imgg2 = cv2.resize(img, (453, 340))
            al = Thread(target=cv2.imshow("wepcam", imgg2))
            al.start()

    def bak(self):
        try:
            cozunurluk = [int(i) for i in self.cozünürlük.currentText().lower().split("x")]

            if cozunurluk[0] >= 3000 or cozunurluk[1] >= 3000:
                self.setWindowTitle("video kaydet  VS_20.10.21  -- ÇÖZÜNÜRLÜK HATASI !!! ")
            else:
                self.setWindowTitle("video kaydet  VS_20.10.21 ")
                self.kayit(cozunurluk)
        except:
            self.setWindowTitle("video kaydet  VS_20.10.21  --- ÇÖZÜNÜRLÜK HATASI !!! ")
    def kontrol_name(self,name,i=1):
        a=name.split("_")
        b=a[0]+"_"+a[1]
        if b+"_"+str(i)+".mp4" in os.listdir():
            i+=1
            self.kontrol_name(name,i=i)
        else:
            self.video_name=b+"_"+str(i)
    def kayit(self,cozunurluk):
        self.saat.start(1000)
        self.saat.timeout.connect(self.zaman_say)
        self.buton.blockSignals(True)
        self.cozünürlük.setEnabled(False)
        self.buton.setIcon(QIcon(""))

        self.buton2.blockSignals(False)
        self.buton2.setIcon(QIcon("durdur.png"))
        # surum 1 £###################
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        # surum 2 #################
        #fourcc = cv2.VideoWriter_fourcc(*"mp4V")


                                                                # gecikme suresi



        self.kontrol_name(self.video_name)
        self.cek = cv2.VideoWriter(self.video_name+".mp4", fourcc,10, tuple(cozunurluk))


        while True:
            # surum 1 ıcın
            if len(sct.monitors) > 2:
                ka=cv2.cvtColor(numpy.array(sct.grab(sct.monitors[int(self.monitor.currentText()[0])])),cv2.COLOR_BGR2RGB)
                ka = cv2.cvtColor(ka, cv2.COLOR_BGR2RGB)
            else:
                ka = cv2.cvtColor(numpy.array(ImageGrab.grab()),cv2.COLOR_BGR2RGB)


            ka=cv2.resize(ka,tuple(cozunurluk))

            kaydet = Thread(target = self.cek.write(ka))
            kaydet.start()

            self.buton2.clicked.connect(self.durdur)

            if cv2.waitKey(1)==ord("q"):
                break
    def durdur(self):
        self.saat.stop()

        self.a=0
        self.b=0
        self.c=0
        say = str(self.a) + ":" + str(self.b) + ":" + str(self.c)
        self.zaman.setText(say)


        self.buton2.blockSignals(True)
        self.buton2.setIcon(QIcon(""))

        self.buton.blockSignals(False)
        self.buton.setIcon(QIcon("basla.png"))
        self.cozünürlük.setEnabled(True)
        self.cek.release()



def main():
    app = QApplication(sys.argv)
    yazı = kaydet()
    yazı.show()
    sys.exit(app.exec_())
main()