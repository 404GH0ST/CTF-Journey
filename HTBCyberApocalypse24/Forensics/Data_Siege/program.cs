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

