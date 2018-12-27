using System;
using System.Collections.Generic;

namespace Crypting
{
    public class Gamma
    {
        public static string Encrypt(string input, string gamma)
        {
            List<int> s1 = ConvertTC.TextToCode(input);
            List<int> s2 = ConvertTC.TextToCode(gamma);

            List<int> it = new List<int>();

            for (int i = 0; i < s1.Count; i++)
            {
                it.Add((s1[i] + s2[i]) % alp.Length);
            }

            return ConvertTC.CodeToText(it);
        }

        public static string Decrypt(string sh, string gamma)
        {
            List<int> s2 = ConvertTC.TextToCode(sh);
            List<int> s3 = ConvertTC.TextToCode(gamma);
            List<int> res = new List<int>();

            for (int i = 0; i < s2.Count; i++)
            {
                res.Add((s2[i] - s3[i] + alp.Length) % alp.Length);
            }

            return ConvertTC.CodeToText(res);
        }

        public static string alp = "¶абвгдеёжзийклмнопрстуфхцчшщьыъэюя" +
                            "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ" +
                            "abcdefghijklmnopqrstuvwxyz" +
                            "ABCDEFGHIJKLMNOPQRSTUVWXYZ" +
                            "0123456789" +
                            ".,!?:-_=+\"\\#№$%^&*;()±§<>{}[] ";
    }
}
