using System;
using System.Collections.Generic;

namespace Crypting
{
    public class ConvertTC
    {
        public static string alp = "¶абвгдеёжзийклмнопрстуфхцчшщьыъэюя" +
                            "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ" +
                            "abcdefghijklmnopqrstuvwxyz" +
                            "ABCDEFGHIJKLMNOPQRSTUVWXYZ" +
                            "0123456789" +
                            ".,!?:-_=+\"\\#№$%^&*;()±§<>{}[] ";

        public static List<int> TextToCode(string s)
        {
            List<int> result = new List<int>();
            result.Clear();

            for (int i = 0; i < s.Length; i++)
            {
                result.Add(alp.IndexOf(s[i]));
            }

            return result;
        }

        public static string CodeToText(List<int> s)
        {
            List<char> res = new List<char>();


            for (int i = 0; i < s.Count; i++)
            {
                res.Add(alp[s[i]]);
            }

            return new string(res.ToArray());
        }
    }
}
