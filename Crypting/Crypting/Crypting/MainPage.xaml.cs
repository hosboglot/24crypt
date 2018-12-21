using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using Xamarin.Forms;
using Xamarin.Essentials;
using Newtonsoft.Json;

namespace Crypting
{
    public partial class MainPage : ContentPage
    {
        static int cryptingTypeInt = -1;
        static int operation = -1;
        string dataFile = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "Data.txt");
        public MainPage()
        {
            InitializeComponent();
            Capi.Source = ImageSource.FromResource("Crypting.vodosvinka-ili-kapibara.jpg");
            KeyEnter.Placeholder = "Введите гамму или оставьте поле пустым для автогенерации...";
            if (!File.Exists(dataFile))
            {
                File.WriteAllText(dataFile, "{\"0\":[0,0]}");
            }
            keys = JsonConvert.DeserializeObject<Dictionary<string, List<int>>>(File.ReadAllText(dataFile));
        }


        private void Picker_SelectedIndexChangedType(object sender, EventArgs e)
        {
            CipherTextLabel.IsVisible = false;
            KeyLabel.IsVisible = false;
            CipherText.IsVisible = false;
            Key.IsVisible = false;
            ErrorLabel.IsVisible = false;
            SwitchBut.IsVisible = false;
            GenRSAKey.IsVisible = false;
            RSAKeyLabel.IsVisible = false;
            RSAOpenKey.IsVisible = false;
            KeyCopy.IsVisible = false;
            MsgCopy.IsVisible = false;
            MsgSend.IsVisible = false;
            OKeySend.IsVisible = false;
            OKeyCopy.IsVisible = false;
            ClearRSAData.IsVisible = false;
            SetOperation.IsEnabled = true;
            LayOut.IsVisible = false;
            LayRSA.IsVisible = false;
            MsgEnter.Text = null;
            KeyEnter.Text = null;

            switch (SetCryptingType.SelectedIndex)
            {
                case 0:
                    cryptingTypeInt = 0;
                    if (operation != -1) SwitchBut.IsVisible = true;
                    KeyEnter.Keyboard = Keyboard.Default;
                    KeyEnter.Placeholder = "Введите гамму или оставьте поле пустым для автогенерации...";
                    break;

                case 1:
                    cryptingTypeInt = 1;
                    KeyEnter.Keyboard = Keyboard.Numeric;
                    KeyEnter.Placeholder = "Введите ключ (целое число)...";
                    break;
            
                case 2:            
                    cryptingTypeInt = 2;
                    KeyEnter.Keyboard = Keyboard.Default;
                    RSAConfig();
                    break;
            }
        }




        //Изменение операции
        private void Picker_SelectedIndexChangedRev(object sender, EventArgs e)
        {
            KeyEnter.IsVisible = true;
            MsgEnter.IsVisible = true;
            Button.IsVisible = true;
            ErrorLabel.IsVisible = false;
            SwitchBut.IsVisible = false;
            GenRSAKey.IsVisible = false;
            RSAKeyLabel.IsVisible = false;
            RSAOpenKey.IsVisible = false;
            ClearRSAData.IsVisible = false;
            LayEnter.IsVisible = true;
            LayRSA.IsVisible = false;
            MsgEnter.Text = null;
            operation = SetOperation.SelectedIndex;

            switch (SetOperation.SelectedIndex)
            {
                case 0:
                    MsgEnter.Placeholder = "Введите сообщение для шифровки...";
                    switch (cryptingTypeInt)
                    {
                        case 0:
                            KeyEnter.Placeholder = "Введите гамму или оставьте поле пустым для автогенерации...";
                            SwitchBut.IsVisible = true;
                            SwitchBut.Text = "Перенести гамму вверх";
                            break;
                        case 1:
                            KeyEnter.Placeholder = "Введите ключ (целое число)...";
                            break;
                        case 2:
                            RSAConfig();
                            break;
                    }
                    break;

                case 1:
                    MsgEnter.Placeholder = "Введите сообщение для расшифровки...";
                    switch (cryptingTypeInt)
                    {
                        case 0:
                            KeyEnter.Placeholder = "Введите гамму...";
                            SwitchBut.IsVisible = true;
                            SwitchBut.Text = "Перенести гамму вверх";
                            break;
                        case 1:
                            KeyEnter.Placeholder = "Введите ключ (целое число)...";
                            break;
                        case 2:
                            RSAConfig();
                            break;
                    }
                    break;
            }
        }



        //Операция
        private void Button_ClickedMsg(object sender, EventArgs e)
        {
            ErrorLabel.IsVisible = false;
            CipherTextLabel.IsVisible = false;
            KeyLabel.IsVisible = false;
            CipherText.IsVisible = false;
            Key.IsVisible = false;
            KeyCopy.IsVisible = false;
            MsgCopy.IsVisible = false;
            MsgSend.IsVisible = false;
            LayOut.IsVisible = true;
            

            switch (operation)
            {
                //Шифровка
                case 0:
                    switch (cryptingTypeInt)
                    {
                        //Гаммирование
                        case 0:
                            if (MsgEnter.Text == null || MsgEnter.Text == "")
                            {
                                ErrorLabel.Text = "Введите сообщение.";
                                ErrorLabel.IsVisible = true;
                                break;
                            }

                            //Генерация гаммы
                            string gamma = KeyEnter.Text;
                            if (gamma == null || gamma == "")
                            {
                                List<char> gamma1 = new List<char>(MsgEnter.Text);
                                Random rnd = new Random();
                                for (int i = 0; i < MsgEnter.Text.Length; i++)
                                {
                                    gamma1[i] = Gamma.alp[rnd.Next(0, Gamma.alp.Length - 1)];
                                }
                                gamma = new string(gamma1.ToArray());
                            }

                            else if (gamma.Length < MsgEnter.Text.Length)
                            {
                                ErrorLabel.Text = "Гамма должна быть больше или равна сообщению.";
                                ErrorLabel.IsVisible = true;
                                break;
                            }

                            CipherText.Text = Gamma.Encrypt(MsgEnter.Text, gamma);
                            Key.Text = gamma;
                            CipherTextLabel.IsVisible = true;
                            KeyLabel.IsVisible = true;
                            CipherText.IsVisible = true;
                            Key.IsVisible = true;
                            KeyCopy.IsVisible = true;
                            MsgCopy.IsVisible = true;
                            MsgSend.IsVisible = true;
                            break;



                        //Цезарь
                        case 1:
                            if (MsgEnter.Text == null || MsgEnter.Text == "")
                            {
                                ErrorLabel.Text = "Введите сообщение.";
                                ErrorLabel.IsVisible = true;
                                break;
                            }

                            int key;
                            if (!int.TryParse(KeyEnter.Text, out key))
                            {
                                ErrorLabel.Text = "Ключ либо введен неправильно, либо отсутствует.";
                                ErrorLabel.IsVisible = true;
                                break;
                            }

                            if (key >= 33)
                            {
                                ErrorLabel.Text = "Ключ должен быть меньше 33.";
                                ErrorLabel.IsVisible = true;
                                break;
                            }

                            CipherText.Text = Ceasar.Encrypt(MsgEnter.Text, key);
                            CipherTextLabel.IsVisible = true;
                            CipherText.IsVisible = true;
                            MsgCopy.IsVisible = true;
                            MsgSend.IsVisible = true;
                            break;



                        //РСА
                        case 2:
                            if (MsgEnter.Text == null || MsgEnter.Text == "")
                            {
                                ErrorLabel.Text = "Введите сообщение.";
                                ErrorLabel.IsVisible = true;
                                break;
                            }

                            if (KeyEnter.Text == null || KeyEnter.Text == "")
                            {
                                ErrorLabel.Text = "Введите открытый ключ.";
                                ErrorLabel.IsVisible = true;
                                break;
                            }

                            string[] RSAkey = KeyEnter.Text.Split(' ');
                            List<int> RSAOpen = new List<int>();
                            try
                            {
                                RSAOpen.Add(int.Parse(RSAkey[0])); RSAOpen.Add(int.Parse(RSAkey[1]));
                            }
                            catch
                            {
                                ErrorLabel.Text = "Ключ должен быть представлен двумя числами.";
                                ErrorLabel.IsVisible = true;
                                break;
                            }

                            CipherText.Text = string.Join(" ", RSA.Encrypt(MsgEnter.Text, RSAOpen));
                            CipherTextLabel.IsVisible = true;
                            CipherText.IsVisible = true;
                            MsgCopy.IsVisible = true;
                            MsgSend.IsVisible = true;
                            break;
                    }
                    break;





                //Расшифровка
                case 1:
                    switch (cryptingTypeInt)
                    {
                        //Гаммирование
                        case 0:
                            if (MsgEnter.Text == null || MsgEnter.Text == "")
                            {
                                ErrorLabel.Text = "Введите зашифрованное сообщение.";
                                ErrorLabel.IsVisible = true;
                                break;
                            }

                            string gamma = KeyEnter.Text;

                            if (gamma == null || gamma == "")
                            {
                                ErrorLabel.Text = "Введите гамму.";
                                ErrorLabel.IsVisible = true;
                                break;
                            }

                            if (gamma.Length < MsgEnter.Text.Length)
                            {
                                ErrorLabel.Text = "Гамма должна быть больше или равна сообщению.";
                                ErrorLabel.IsVisible = true;
                                break;
                            }

                            CipherText.Text = Gamma.Decrypt(MsgEnter.Text, gamma);
                            CipherTextLabel.IsVisible = true;
                            CipherText.IsVisible = true;
                            break;



                        //Цезарь
                        case 1:
                            if (MsgEnter.Text == null || MsgEnter.Text == "")
                            {
                                ErrorLabel.Text = "Введите зашифрованное сообщение.";
                                ErrorLabel.IsVisible = true;
                                break;
                            }

                            int key;
                            if (!int.TryParse(KeyEnter.Text, out key))
                            {
                                ErrorLabel.Text = "Ключ либо введен неправильно, либо отсутствует.";
                                ErrorLabel.IsVisible = true;
                                break;
                            }

                            CipherText.Text = Ceasar.Decrypt(MsgEnter.Text, key);
                            CipherTextLabel.IsVisible = true;
                            CipherText.IsVisible = true;
                            break;



                        //РСА
                        case 2:
                            if (MsgEnter.Text == null || MsgEnter.Text == "")
                            {
                                ErrorLabel.Text = "Введите сообщение.";
                                ErrorLabel.IsVisible = true;
                                break;
                            }

                            if (KeyEnter.Text == null || KeyEnter.Text == "")
                            {
                                ErrorLabel.Text = "Введите открытый ключ.";
                                ErrorLabel.IsVisible = true;
                                break;
                            }

                            string[] RSAkey = KeyEnter.Text.Split(' ');
                            List<int> RSAOpen = new List<int>();
                            try
                            {
                                RSAOpen.Add(int.Parse(RSAkey[0])); RSAOpen.Add(int.Parse(RSAkey[1]));
                            }
                            catch
                            {
                                ErrorLabel.Text = "Ключ должен быть представлен двумя числами.";
                                ErrorLabel.IsVisible = true;
                                break;
                            }

                            string[] RSAmsg = MsgEnter.Text.Split(' ');
                            List<int> RSAmsgS = new List<int>();
                            try
                            {
                                for (int i = 0; i < RSAmsg.Length; i++)
                                {
                                    RSAmsgS.Add(int.Parse(RSAmsg[i]));
                                }
                            }
                            catch
                            {
                                ErrorLabel.Text = "Сообщение должно быть представлено последовательностью чисел, разделенных пробелом.";
                                ErrorLabel.IsVisible = true;
                                break;
                            }
                            
                            if (!keys.ContainsKey(string.Join(" ", RSAOpen)))
                            {
                                ErrorLabel.Text = "Такого ключа нет в данных.";
                                ErrorLabel.IsVisible = true;
                                break;
                            }

                            List<int> RSAClosed = keys[string.Join(" ", RSAOpen)];
                            CipherText.Text = RSA.Decrypt(RSAmsgS, RSAClosed);
                            CipherTextLabel.IsVisible = true;
                            CipherText.IsVisible = true;
                            break;
                    }
                    break;
            }
        }

        //Перенести ключ вверх
        private void SwitchBut_Clicked(object sender, EventArgs e)
        {
            if (cryptingTypeInt == 2) KeyEnter.Text = RSAOpenKey.Text;
            else KeyEnter.Text = Key.Text;
        }
        
        //Генерация РСА ключей
        Dictionary<string, List<int>> keys = new Dictionary<string, List<int>>();
        private void GenRSAKey_Clicked(object sender, EventArgs e)
        {
            List<int> RSAClosed = new List<int>();
            List<int> RSAOpen = new List<int>();
            RSA.GenKey(out RSAOpen, out RSAClosed);
            RSAOpenKey.Text = string.Join(" ", RSAOpen);
            try
            {
                keys.Add(string.Join(" ", RSAOpen), RSAClosed);
            }
            catch
            {
                keys = new Dictionary<string, List<int>>{ { string.Join(" ", RSAOpen), RSAClosed } };
            }
            File.WriteAllText(dataFile, JsonConvert.SerializeObject(keys));
            OKeySend.IsVisible = true;
            OKeyCopy.IsVisible = true;
        }

        //Кофнигурация РСА
        void RSAConfig()
        {
            if (operation == 1) KeyEnter.Placeholder = "Вставьте ваш открытый ключ...";
            if (operation == 0) KeyEnter.Placeholder = "Скопируйте ключ, отправленный вам собеседником...";
            GenRSAKey.IsVisible = true;
            RSAKeyLabel.IsVisible = true;
            RSAOpenKey.IsVisible = true;
            LayRSA.IsVisible = true;
            ClearRSAData.IsVisible = true;
            if (operation != -1)
            {
                SwitchBut.IsVisible = true;
                SwitchBut.Text = "Перенести открытый ключ вверх";
            }
            if (!(RSAOpenKey.Text == null || RSAOpenKey.Text == ""))
            {
                OKeySend.IsVisible = true;
                OKeyCopy.IsVisible = true;
            }
        }

        //Скопировать сообщение
        private void MsgCopy_Clicked(object sender, EventArgs e)
        {
            Clipboard.SetTextAsync(CipherText.Text);
        }

        //Отправить сообщение
        private void MsgSend_Clicked(object sender, EventArgs e)
        {
            Share.RequestAsync(new ShareTextRequest
            {
                Text = CipherText.Text,
                Title = "Отправить сообщение..."
            });
        }

        //Скопировать ключ
        private void KeyCopy_Clicked(object sender, EventArgs e)
        {
            Clipboard.SetTextAsync(Key.Text);
        }

        //Отправить открытый ключ
        private void OKeySend_Clicked(object sender, EventArgs e)
        {
            Share.RequestAsync(new ShareTextRequest
            {
                Text = RSAOpenKey.Text,
                Title = "Поделиться ключом..."
            });
        } 

        //Скопировать открытый ключ
        private void OKeyCopy_Clicked(object sender, EventArgs e)
        {
            Clipboard.SetTextAsync(RSAOpenKey.Text);
        }

        //Удалить файл с ключами
        private void ClearRSAData_Clicked(object sender, EventArgs e)
        {
            File.Delete(dataFile);
            File.WriteAllText(dataFile, "{\"0\":[0,0]}");
        }
    }
}
