using System;
using System.Collections.Generic;

namespace Timur
{
    class Crypting
    {
        static void Main()
        {
            Console.WriteLine("Set crypting type: \n" +
                              "1 - RSA\n" +
                              "2 - Gamma\n" +
                              "3 - Ceasar");

            string cryptType = Console.ReadLine();
            if(cryptType == "1")
            {
                Console.WriteLine("RSA is set.\n\n" +
                                  "Input 2 non-complicated numbers.");
                List<int> Okeys = new List<int>();
                List<int> Ckeys = new List<int>();

                int a = Int32.Parse(Console.ReadLine());
                int b = Int32.Parse(Console.ReadLine());
                RSA.GenKey(a, b, out Okeys, out Ckeys);

                Console.WriteLine("\nYour open keys is: " + Okeys[0] + " " +Okeys[1] +
                                  "\nInput your message: ");
                
                string msg = Console.ReadLine();
                List<int> ci = RSA.Encrypt(msg, Ckeys);

                Console.WriteLine("\nYour ciphertext is: ");

                ci.ForEach(Console.WriteLine);

                Console.WriteLine("\nYour decrypted text is: " + RSA.Decrypt(ci, Okeys));
            }



            else if (cryptType == "2")
            {
                Console.WriteLine("Gamma is set\n\n" +
                                  "Input your message.");

                string input = Console.ReadLine();

                Console.WriteLine("\nInput your gamma or input \"!random\" to set random gamma");

                string ans = Console.ReadLine();
                string gamma;
                Console.WriteLine();
                if (ans == "!random")
                {
                    List<char> gamma1 = new List<char>(input);
                    Random rnd = new Random();
                    for (int i = 0; i < input.Length; i++)
                    {
                        gamma1[i] = Gamma.alp[rnd.Next(0, Gamma.alp.Length - 1)];
                    }
                    gamma = new string (gamma1.ToArray());
                    Console.WriteLine("Your gamma is: \n" + gamma);
                }

                else
                {
                    gamma = ans;
                }

                string ci = Gamma.Encrypt(input, gamma);
                Console.WriteLine("\nYour ciphertext is: \n" + ci +
                                  "\nYour decrypted text is: \n" + Gamma.Decrypt(ci, gamma));
            }



            else
            {
                Console.WriteLine("Ceasar is set\n\n" +
                                  "Input your message.");

                string input = Console.ReadLine();

                Console.WriteLine("\nInput the key (must be a number)");

                int key = Int32.Parse(Console.ReadLine());

                string ci = Ceasar.Encrypt(input, key);

                Console.WriteLine("\nYour ciphertext is: \n" + ci);

                Console.WriteLine("\nYour decrypted text is: \n" + Ceasar.Decrypt(ci, key));
            }
        }
    }
}
