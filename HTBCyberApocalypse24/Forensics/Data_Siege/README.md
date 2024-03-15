# Solver
You could analyze the file using `NetworkMiner` to get the general overview, but we need to convert it to pcap format first.

```bash
editcap -F pcap capture.pcap out.pcap
```

From the NetworkMiner miner Sessions tab, looks like this capture file contains Reverse Shell traffic.

We could get the implant file by viewing th 4th TCP Stream. Running the program with `DetectItEasy` reveals that this program is compiled with `.NET`. I will use `AvalonialSpy` to decompile this program.

From there, we will get this is a [EZRAT](https://github.com/Exo-poulpe/EZRAT) program. In this program the traffic is encrypted with AES, but the encryption key itself is embedded in the program.

Then, I a simple decryption program using [Program.cs](https://github.com/Exo-poulpe/EZRAT/blob/master/EZRATClient/Program.cs) as reference.

```c#
using System;
using System.IO;
using System.Security.Cryptography;
using System.Text;

class Program
{
    static string EncryptKey = "VYAemVeO3zUDTL6N62kVA"; // Set your secret encryption key here

    public static string Decrypt(string cipherText)
    {
        try
        {
            string EncryptionKey = EncryptKey; // this is the secret encryption key you want to hide, don't show it to others
            byte[] cipherBytes = Convert.FromBase64String(cipherText); // Get the encrypted message's bytes
            using (Aes encryptor = Aes.Create()) // Create a new AES object
            {
                // Decrypt the text
                Rfc2898DeriveBytes pdb = new Rfc2898DeriveBytes(EncryptionKey, new byte[] { 86, 101, 114, 121, 95, 83, 51, 99, 114, 51, 116, 95, 83 });
                encryptor.Key = pdb.GetBytes(32);
                encryptor.IV = pdb.GetBytes(16);
                using (MemoryStream ms = new MemoryStream())
                {
                    using (CryptoStream cs = new CryptoStream(ms, encryptor.CreateDecryptor(), CryptoStreamMode.Write))
                    {
                        cs.Write(cipherBytes, 0, cipherBytes.Length);
                    }
                    cipherText = Encoding.Default.GetString(ms.ToArray());
                }
            }
            return cipherText; // Return the plain text data
        }
        catch (Exception ex) // Something went wrong
        {
            Console.WriteLine(ex.Message);
            Console.WriteLine("Cipher Text: " + cipherText);
            return "error"; // Return error
        }
    }

    static void Main(string[] args)
    {
        // Test the Decrypt method
        string encryptedText = args[0];
        string decryptedText = Decrypt(encryptedText);
        Console.WriteLine("Decrypted Text: " + decryptedText);
    }
}
```

You can start decoding encrypted traffic in the 5th TCP Stream

Eventually, you will get the first and second part of the flag from the encrypted traffic. For the third part of the flag, you can get it from the PowerShell encoded command.

