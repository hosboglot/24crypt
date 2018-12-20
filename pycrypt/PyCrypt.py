import sys
import os
from random import randint
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QCheckBox

# алфавит
global alp
alp = "абвгдеёжзийклмнопрстуфхцчшщьыъэюя" \
      "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ" \
      "abcdefghijklmnopqrstuvwxyz" \
      "ABCDEFGHIJKLMNOPQRSTUVWXYZ" \
      "0123456789" \
      ".,!?:-_=+\/#№$%^&*;()±§<>{}[] " \
      "\""
# список простых чисел
global fabInt
fabInt = [
    97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181,
    191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283,
    293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409,
    419, 421, 431, 433, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503
]


# функция вставки строки в буфер обмена(работоспособность проверена только на винде)
def addToClipBoard(text):
    command = 'echo | set /p nul=' + text.strip() + '| clip'
    os.system(command)


# класс конвертации из текста в шифр-текст и из шифр-текста в текст
# используется как база для всего остального алгоритма шифрования
class ConvertTC:
    def TextToCode(self, string):
        res = []

        for i in range(len(string)):
            res.append(alp.index(string[i]))
        return res

    def CodeToText(self, arr):
        res = []

        for i in range(len(arr)):
            res.append(alp[arr[i]])
        return ''.join(res)


Convert = ConvertTC()


# класс для генерации ключей, зашифровки и расшифровки информации
# по методу RSA
class RSA:
    # проверка в GenKeys(смотрите метод ниже)
    def ChSim(self, a, b):
        while a != b:
            if a > b:
                a -= b
            else:
                b -= a

        if a == 1:
            return True
        return False

    # герация ключей(всё по алгоритму из википедии)
    def GenKey(self, a, b):
        n = a * b
        eil = (a - 1) * (b - 1)
        simple = randint(1, int(eil))

        while not self.ChSim(eil, simple):
            simple = randint(1, int(eil))

        d = 1
        while ((d * simple) % eil) != 1:
            d += 1

        Opkeys = [int(simple), int(n)]
        Clkeys = [d, int(n)]
        return [Opkeys, Clkeys]

    # зашифровка
    def Encrypt(self, inp, keys):
        text = Convert.TextToCode(inp)
        res = []

        for i in range(len(inp)):
            res.append(int((text[i] ** keys[0]) % keys[1]))
        return res

    # расшифровка
    def Decrypt(self, inp, keys):
        res = []

        for i in range(len(inp)):
            res.append(int((inp[i] ** keys[0]) % keys[1]))
        return Convert.CodeToText(res)


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        # загрузка формы GUI
        uic.loadUi('PyCryptGUI.ui', self)

        # объявление экземпляра класса RSA для работы
        self.RSAA = RSA()
        # индикатор: сохранять ключи в файл или нет
        self.saveInFile = False
        # индикатор: сгенерировать числа или нет
        self.genNumsPy = False
        # индикатор: пасхалочка
        self.DV = False
        # индикатор: пасхалочка
        self.PyLove = False

        # подключение функций к кнопкам
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
            print(key, msg)
            self.decText = self.RSAA.Decrypt(msg, key)
            print(self.decText)
            self.getForX.setText(self.decText)
        except BaseException as aaa:
            self.warning.setText("Что-то пошло не так(Расшифровка)")
            print(aaa)


try:
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
except Exception as e:
    print(e)
