# -*- coding: utf-8 -*-
# Steganografi tekniğiyle resim içine mesaj gizleyip, gizli mesajları ortaya çıkarır.
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets
import cv2                  # pip install opencv-python
import numpy as np          # pip install numpy


class Ui_Form(object):
    def __init__(self):
        pass

    def openfile(self):
        self.name = QFileDialog.getOpenFileName()

    def cevirBinary(self, bilgi):
        if type(bilgi) == str:
            return ''.join([format(ord(i), "08b") for i in bilgi])
        elif type(bilgi) == bytes or type(bilgi) == np.ndarray:
            return [format(i, "08b") for i in bilgi]
        elif type(bilgi) == int or type(bilgi) == np.uint8:
            return format(bilgi, "08b")
        else:
            raise TypeError("Girdi türü desteklenmiyor.")

    def bilgiGizle(self, image, secret_message):
        # kodlanacak maksimum bayt hesapla
        n_bytes = image.shape[0] * image.shape[1] * 3 // 8
        # Kodlanacak bayt sayısının görüntüdeki maksimum bayttan az olup olmadığını kontrol edin
        if len(secret_message) > n_bytes:
            raise ValueError("Hata yetersiz baytlarla karşılaştı, daha büyük görüntü veya daha az veri gerekiyor!")
        secret_message += "#####"  # sınırlayıcı olarak herhangi bir dizeyi kullanabilirsiniz
        data_index = 0
        # cevirBinary() işlevini kullanarak giriş verilerini ikili biçime dönüştürme
        binary_secret_msg = self.cevirBinary(secret_message)
        data_len = len(binary_secret_msg)  # Gizlenmesi gereken verilerin uzunluğunu bulun
        for values in image:
            for pixel in values:
                # RGB değerlerini ikili biçime dönüştürme
                r, g, b = self.cevirBinary(pixel)
                # en az anlamlı biti yalnızca saklanacak veriler varsa değiştirin
                if data_index < data_len:
                    # verileri en az anlamlı kırmızı piksel bitine sakla
                    pixel[0] = int(r[:-1] + binary_secret_msg[data_index], 2)
                    data_index += 1
                if data_index < data_len:
                    # verileri en az anlamlı yeşil piksel bitine sakla
                    pixel[1] = int(g[:-1] + binary_secret_msg[data_index], 2)
                    data_index += 1
                if data_index < data_len:
                    # verileri en az anlamlı mavi piksel bitine sakla
                    pixel[2] = int(b[:-1] + binary_secret_msg[data_index], 2)
                    data_index += 1
                # eğer veri kodlanmışsa, döngüden çıkın
                if data_index >= data_len:
                    break
        return image

    def bilgiGoster(self, image):
        try:
            binary_data = ""
            for values in image:
                for pixel in values:
                    r, g, b = self.cevirBinary(pixel)  # kırmızı, yeşil ve mavi değerleri ikili biçime dönüştürür
                    binary_data += r[-1]  # en az anlamlı kırmızı piksel bitinden veri çıkarma
                    binary_data += g[-1]  # en az anlamlı yeşil piksel bitinden veri çıkarma
                    binary_data += b[-1]  # en az anlamlı mavi piksel bitinden veri çıkarma
            # split by 8-bits
            all_bytes = [binary_data[i: i + 8] for i in range(0, len(binary_data), 8)]
            # bitlerden karakterlere dönüştür
            decoded_data = ""
            for byte in all_bytes:
                decoded_data += chr(int(byte, 2))
                if decoded_data[-5:] == "#####":  # "#####" sınırlayıcısına ulaşıp ulaşmadığımızı kontrol edin
                    break
            return decoded_data[:-5]  # orijinal gizli mesajı göstermek için ayırıcıyı kaldırın
        except:
            QtWidgets.QMessageBox.warning(self, "ERROR", "Bir Hata Oluştu")

    # Verileri görüntüye kodlama
    def kodlayici(self):
        image = cv2.imread(self.name[0])  # OpenCV-Python kullanarak giriş görüntüsünü okuyun.
        data = self.textEdit.toPlainText()
        data = data.replace("ı", "i")
        data = data.replace("ö", "o")
        data = data.replace("İ", "I")
        data = data.replace("ü", "u")
        data = data.replace("ç", "c")
        data = data.replace("Ç", "C")
        if len(data) == 0:
            raise ValueError('Veri boş')
        # gizli mesajı seçilen görüntüye gizlemek için bilgiGizle işlevini çağırın
        encoded_image = self.bilgiGizle(image, data)
        cv2.imwrite(self.name[0], encoded_image)

    # Görüntüdeki verilerin kodunu çözme
    def kodCoz(self):
        try:
            image = cv2.imread(self.name[0])  # cv2.imread () kullanarak görüntüyü okuyun
            text = self.bilgiGoster(image)
            self.textEdit.setFontPointSize(12)
            self.textEdit.setText(text)
        except:
            QtWidgets.QMessageBox.warning(self, "ERROR", "Bir Hata Oluştu")

    def setupUi(self, Form):
        try:
            Form.setStyleSheet("background-color: #cdb38b")
            Form.setObjectName("Form")
            Form.resize(788, 570)
            self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
            self.verticalLayout_2.setObjectName("verticalLayout_2")
            self.verticalLayout = QtWidgets.QVBoxLayout()
            self.verticalLayout.setObjectName("verticalLayout")
            self.verticalLayout_2.addLayout(self.verticalLayout)
            self.pushButton = QtWidgets.QPushButton(Form)
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.pushButton.setFont(font)
            self.pushButton.setObjectName("pushButton")
            self.verticalLayout_2.addWidget(self.pushButton)
            self.pushButton.clicked.connect(self.openfile)
            self.textEdit = QtWidgets.QTextEdit(Form)
            self.textEdit.setWhatsThis("")
            self.textEdit.setAccessibleDescription("")
            self.textEdit.setLayoutDirection(QtCore.Qt.LeftToRight)
            self.textEdit.setFrameShape(QtWidgets.QFrame.Box)
            self.textEdit.setFrameShadow(QtWidgets.QFrame.Plain)
            self.textEdit.setDocumentTitle("")
            self.textEdit.setObjectName("textEdit")
            self.textEdit.setFontPointSize(12)
            self.textEdit.setStyleSheet("background-color: #cd9b9b")
            self.verticalLayout_2.addWidget(self.textEdit)
            self.pushButton_2 = QtWidgets.QPushButton(Form)
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.pushButton_2.setFont(font)
            self.pushButton_2.setFocusPolicy(QtCore.Qt.StrongFocus)
            self.pushButton_2.setWhatsThis("")
            self.pushButton_2.setObjectName("pushButton_2")
            self.verticalLayout_2.addWidget(self.pushButton_2)
            self.pushButton_2.clicked.connect(self.kodlayici)
            self.pushButton_3 = QtWidgets.QPushButton(Form)
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.pushButton_3.setFont(font)
            self.pushButton_3.setObjectName("pushButton_3")
            self.verticalLayout_2.addWidget(self.pushButton_3)
            self.pushButton_3.clicked.connect(self.kodCoz)

            self.retranslateUi(Form)
            QtCore.QMetaObject.connectSlotsByName(Form)
        except:
            QtWidgets.QMessageBox.warning(self, "ERROR", "Bir Hata Oluştu")

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "STEGANOGRAFİ"))
        self.pushButton.setText(_translate("Form", "Dosya Seç (.png)"))
        self.pushButton_2.setText(_translate("Form", "Mesaj Gizle"))
        self.pushButton_3.setText(_translate("Form", "Mesaj Göster"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
