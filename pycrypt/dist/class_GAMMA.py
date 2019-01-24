import class_convert
import string
from random import choices

# иницилизация класса конвертации
Convert = class_convert.ConvertTC()
alp = class_convert.alp


# # класс для генерации ключа, зашифровки и расшифровки информации
# # методом гаммирования
class Gamma:
    # генерация ключа
    def genGamma(self, N):
        res = ''.join(choices(string.ascii_uppercase + string.digits, k=N))
        return res

    # зашифровка
    def Encrypt(self, inp, gam):
        inp = Convert.TextToCode(inp)
        gam = Convert.TextToCode(gam)
        res = []
        [res.append((inp[i] + gam[i]) % len(class_convert.alp)) for i in range(len(inp))]
        return Convert.CodeToText(res)

    # расшифровка
    def Decrypt(self, ci, gam):
        ci = Convert.TextToCode(ci)
        gam = Convert.TextToCode(gam)
        res = []
        [res.append((ci[i] - gam[i] + len(alp)) % len(alp)) for i in range(len(ci))]
        return Convert.CodeToText(res)
