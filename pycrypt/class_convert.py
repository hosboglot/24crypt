# алфавит
global alp
file = open("alp.txt", 'r')
alp = file.read()
file.close()

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