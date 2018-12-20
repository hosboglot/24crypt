using System;
using System.Collections.Generic;

namespace Crypting
{
    public class Ceasar
    {
        static string alpRus = "абвгдеёжзийклмнопрстуфхцчшщьыъэюя";
        static string alpEng = "abcdefghijklmnopqrstuvwxyz";

        static public string Encrypt(string input, int key)
        {
            input = input.ToLower();
            string result = "";

            for (int i = 0; i < input.Length; i++)
            {
                if (alpRus.Contains(input[i].ToString()))
                {
                    int code = alpRus.IndexOf(input[i]);
                    code += key;
                    if (code < 0) code = alpRus.Length + code;
                    if (code >= alpRus.Length) code = code - alpRus.Length;
                    result += alpRus[code].ToString();
                }

                else if (alpEng.Contains(input[i].ToString()))
                {
                    int code = alpEng.IndexOf(input[i]);
                    code += key;
                    if (code < 0) code = alpEng.Length + code;
                    if (code >= alpEng.Length) code = code - alpEng.Length;
                    result += alpEng[code].ToString();
                }

                else result += input[i];
            }

            return result;
        }

        static public string Decrypt(string input, int key)
        {
            input = input.ToLower();
            string result = "";
            key *= -1;

            for (int i = 0; i < input.Length; i++)
            {
                if (alpRus.Contains(input[i].ToString()))
                {
                    int code = alpRus.IndexOf(input[i]);
                    code += key;
                    if (code < 0) code = alpRus.Length + code;
                    if (code >= alpRus.Length) code = code - alpRus.Length;
                    result += alpRus[code].ToString();
                }

                else if (alpEng.Contains(input[i].ToString()))
                {
                    int code = alpEng.IndexOf(input[i]);
                    code += key;
                    if (code < 0) code = alpEng.Length + code;
                    if (code >= alpEng.Length) code = code - alpEng.Length;
                    result += alpEng[code].ToString();
                }

                else result += input[i];
            }

            return result;
        }
    }
}
