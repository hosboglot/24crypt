import class_convert

# иницилизация класса конвертации
Convert = class_convert.ConvertTC()
alp = class_convert.alp


class Caesar:
    def Encrypt(self, sd, msg):
        stMsg = Convert.TextToCode(msg)
        endMsg = [i + sd for i in stMsg]
        return Convert.CodeToText(endMsg)

    def Decrypt(self, sd, msg):
        stMsg = Convert.TextToCode(msg)
        endMsg = [i - sd for i in stMsg]
        print(stMsg, endMsg)
        return Convert.CodeToText(endMsg)

