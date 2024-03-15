# Solver
According to wireshark statistic, there's a little conversation using HTTP protocol but let's use it as filter.
There http requests to GET `/freediscordnitro` and POST `/rj1893rj1joijdkajwda`
The `/freediscordnitro` contain a PowerShell script in the response

You can run it and see `$LOaDcODEoPX3ZoUgP2T6cvl3KEK` to get the script content and there's a `$part1` variable that contain base64 part of the flag.

After analyzing the code, I learned that this script will send a POST request to `/rj1893rj1joijdkajwda` with AES encoded data.
We can grab the data from the wireshark and decrypt it. I use this [website](https://www.devglan.com/online-tools/aes-encryption-decryption) to decrypt the data.
The remaining part of the flag should be inside the decrypted data.
