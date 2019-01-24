import sys
import os
from random import randint
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QCheckBox
import class_RSA
import class_GAMMA
import class_CAESAR

# список простых чисел
global fabInt
fabInt = [
    89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181,
    191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283,
    293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409,
    419, 421, 431, 433, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547,
    557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659,
    661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 739, 743,
    751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877,
    881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013,
    1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069, 1087, 1091, 1093, 1097, 1103, 1109,
    1117, 1123, 1129, 1151, 1153, 1163, 1171, 1181, 1187, 1193, 1201, 1213, 1217, 1223, 1229, 1231,
    1237, 1249, 1259, 1277, 1279, 1283, 1289, 1291, 1297, 1301, 1303, 1307, 1319, 1321, 1327, 1361,
    1367, 1373, 1381, 1399, 1409, 1423, 1427, 1429, 1433, 1439, 1447, 1451, 1453, 1459, 1471, 1481,
    1483, 1487, 1489, 1493, 1499, 1511, 1523, 1531, 1543, 1549, 1553, 1559, 1567, 1571, 1579, 1583,
    1597, 1601, 1607, 1609, 1613, 1619, 1621, 1627, 1637, 1657, 1663, 1667, 1669, 1693, 1697, 1699,
    1709, 1721, 1723, 1733, 1741, 1747, 1753, 1759, 1777, 1783, 1787, 1789, 1801, 1811, 1823, 1831,
    1847, 1861, 1867, 1871, 1873, 1877, 1879, 1889, 1901, 1907, 1913, 1931, 1933, 1949, 1951, 1973,
    1979, 1987, 1993, 1997, 1999, 2003, 2011, 2017, 2027, 2029, 2039, 2053, 2063, 2069, 2081, 2083
]


# функция вставки строки в буфер обмена(работоспособность проверена только на винде)
def addToClipBoard(text):
    command = 'echo | set /p nul=' + text.strip() + '| clip'
    os.system(command)


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        # загрузка формы GUI
        uic.loadUi('PyCryptGUI.ui', self)

        # объявление экземпляра класса RSA для работы с RSA
        self.RSAA = class_RSA.RSA()
        # объявление экземпляра класса GMA для работы с гаммированием
        self.GMA = class_GAMMA.Gamma()

        self.Ca = class_CAESAR.Caesar()
        # индикатор: сохранять ключи в файл или нет
        self.saveInFile = False
        # индикатор: сгенерировать числа или нет
        self.genNumsPy = False
        # индикатор: пасхалочка
        self.DV = False
        # индикатор: пасхалочка
        self.PyLove = False
        # индикатор: сохранять гамму в файл или нет
        self.saveGam = False

        # подключение функций к интерфейсу
        self.pushAB.clicked.connect(self.setAB)
        self.generateKeys.clicked.connect(self.genKeys)
        self.copyPub.clicked.connect(self.copyBufPub)
        self.copyPriv.clicked.connect(self.copyBufPriv)
        self.copyTextEnc.clicked.connect(self.copyTextE)
        self.copyTextDec.clicked.connect(self.copyTextD)
        self.fileSave.stateChanged.connect(self.checkFileSave)
        self.genNums.stateChanged.connect(self.genNumbers)
        self.A_M.stateChanged.connect(self.checkDV)
        self.PyCheck.stateChanged.connect(self.checkPyLove)
        self.pushKeyToX.clicked.connect(self.encStart)
        self.pushKeyForX.clicked.connect(self.decStart)
        self.GenGamBut.clicked.connect(self.genGam)
        self.copyGam.clicked.connect(self.copyGamKey)
        self.checkFileGam.stateChanged.connect(self.saveFileGam)
        self.encGamStart.clicked.connect(self.EncryptGam)
        self.decGamStart.clicked.connect(self.DecryptGam)
        self.copyEncMsgGam.clicked.connect(self.copyMsgEncGam)
        self.copyDecMsgGam.clicked.connect(self.copyMsgDecGam)
        self.CeStartE.clicked.connect(self.EncryptCa)
        self.CeStartD.clicked.connect(self.DecryptCa)
        self.copyEce.clicked.connect(self.copyCaE)
        self.copyDce.clicked.connect(self.copyCaD)

    # ввод простых чисел для генерации ключей
    def setAB(self):
        try:
            if not self.genNumsPy:
                self.a = int(self.anum.text())
                self.b = int(self.bnum.text())
            else:
                self.a = fabInt[randint(0, len(fabInt) - 1)]
                self.b = fabInt[randint(0, len(fabInt) - 1)]
                self.anum.setText(str(self.a))
                self.bnum.setText(str(self.b))
        except BaseException:
            self.warning.setText("Что-то пошло не так(Числа)")

    # генерация ключей
    def genKeys(self):
        try:
            gen = self.RSAA.GenKey(self.a, self.b)
            print(self.a, self.b)
            self.Okeys = gen[0]
            self.Okeys = str(self.Okeys[0]) + ' ' + str(self.Okeys[1])
            print(12)
            self.Ckeys = gen[1]
            print(12)
            self.Ckeys = str(self.Ckeys[0]) + ' ' + str(self.Ckeys[1])
            print(self.Ckeys)
            if not self.saveInFile:
                self.publicKey.setText("Ваш публичный ключ: " + self.Okeys)
                self.privateKey.setText("Ваш приватный ключ: " + self.Ckeys)
            else:
                fPub = open("PublicKey.txt", 'w')
                fPub.write(self.Okeys)
                fPub.close()
                fPriv = open("PrivateKey.txt", 'w')
                fPriv.write(self.Ckeys)
                fPriv.close()
                self.warning.setText("Ключи сохранены в папке с программой")
        except BaseException:
            self.warning.setText("Что-то пошло не так(Генерация ключей)")

    # методы копирования строк из label`ов
    def copyBufPub(self):
        try:
            addToClipBoard(self.Okeys)
            if self.DV:
                self.warning.setText("Deus Vult")
        except BaseException:
            self.warning.setText("Нечего копировать")

    def copyBufPriv(self):
        try:
            addToClipBoard(self.Ckeys)
            if self.PyLove:
                self.warning.setText("One Love")
        except BaseException:
            self.warning.setText("Нечего копировать")

    def copyTextE(self):
        try:
            addToClipBoard(self.ci)
        except BaseException:
            self.warning.setText("Нечего копировать")

    def copyTextD(self):
        try:
            addToClipBoard(self.decText)
        except BaseException:
            self.warning.setText("Нечего копировать")

    # чекбокс на генерацию простых чисел
    def genNumbers(self, state):
        if state == QtCore.Qt.Checked:
            self.genNumsPy = True
        else:
            self.genNumsPy = False

    # чекбокс на индикатор сохранения ключей в файл
    def checkFileSave(self, state):
        if state == QtCore.Qt.Checked:
            self.saveInFile = True
        else:
            self.saveInFile = False

    # чекбокс на пасхалчку)))
    def checkDV(self, state):
        if state == QtCore.Qt.Checked:
            self.DV = True
        else:
            self.DV = False

    # чекбокс на пасхалчку)))
    def checkPyLove(self, state):
        if state == QtCore.Qt.Checked:
            self.PyLove = True
        else:
            self.PyLove = False

    # зашифровка
    def encStart(self):
        try:
            key = [int(i) for i in self.getToXkey.text().split()]
            msg = self.msgEnc.text()
            self.ci = ' '.join([str(i) for i in self.RSAA.Encrypt(msg, key)])
            self.getToX.setText(self.ci)
        except BaseException:
            self.warning.setText("Что-то пошло не так(Зашифровка)")

    # расшифровка
    def decStart(self):
        try:
            key = [int(i) for i in self.getForXkey.text().split()]
            msg = [int(i) for i in self.msgDec.text().split()]
            self.decText = self.RSAA.Decrypt(msg, key)
            self.getForX.setText(self.decText)
        except BaseException as exec:
            self.warning.setText("Что-то пошло не так(Расшифровка)")
            print(exec)

    def genGam(self):
        try:
            lenOfGam = int(self.lenGam.text())
            self.sgenGam = self.GMA.genGamma(lenOfGam)
            if not self.saveGam:
                self.GenGamWin.setText(self.sgenGam)
            else:
                file = open("Gamma.txt", "w")
                file.write(self.sgenGam)
                file.close()
                self.warningGam.setText("Гамма теперь в папке с программой")
        except BaseException:
            self.warningGam.setText("Ошибка генерации")

    def copyGamKey(self):
        try:
            addToClipBoard(self.sgenGam)
        except BaseException:
            self.warningGam.setText("Нечего копировать")

    def saveFileGam(self, state):
        if state == QtCore.Qt.Checked:
            self.saveGam = True
        else:
            self.saveGam = False

    def EncryptGam(self):
        try:
            gam = self.gmaEncInp.text()
            msg = self.msgGamEncInp.text()
            self.resEncGam = self.GMA.Encrypt(msg, gam)
            self.getCiGam.setText(self.resEncGam)
        except BaseException:
            self.warningGam.setText("Ошибка зашифровки")

    def copyMsgEncGam(self):
        try:
            addToClipBoard(self.resEncGam)
        except BaseException:
            self.warningGam.setText("Нечего копировать")

    def DecryptGam(self):
        try:
            gam = self.gmaEncInp.text()
            msg = self.msgGamDecInp.text()
            self.resDecGam = self.GMA.Decrypt(msg, gam)
            self.getResGam.setText(self.resDecGam)
        except BaseException:
            self.warningGam.setText("Ошибка дешифровки")

    def copyMsgDecGam(self):
        try:
            addToClipBoard(self.resDecGam)
        except BaseException:
            self.warningGam.setText("Нечего копировать")

    def EncryptCa(self):
        try:
            sd = int(self.sdvig.text())
            msg = self.CeMsgE.text()
            res = self.Ca.Encrypt(sd, msg)
            self.CeMsgEout.setText(res)
        except BaseException:
            self.warningCe.setText("Ошибка зашифровки")

    def DecryptCa(self):
        try:
            sd = int(self.sdvig.text())
            msg = self.CeMsgD.text()
            res = self.Ca.Decrypt(sd, msg)
            self.CeMsgDout.setText(res)
        except BaseException:
            self.warningCe.setText("Ошибка расшифровки")

    def copyCaE(self):
        try:
            addToClipBoard(self.CeMsgEout.text())
        except BaseException:
            self.warningCe.setText("Нечего копировать")

    def copyCaD(self):
        try:
            addToClipBoard(self.CeMsgDout.text())
        except BaseException:
            self.warningCe.setText("Нечего копировать")


try:
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
except Exception as ex:
    print(ex)
