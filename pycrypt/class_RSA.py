import class_convert
from random import randint

# иницилизация класса конвертации
Convert = class_convert.ConvertTC()


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

    # генерация ключей(всё по алгоритму из википедии)
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
