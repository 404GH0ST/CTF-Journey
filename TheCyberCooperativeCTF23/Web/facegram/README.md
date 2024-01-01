# Solution

## SQL Injection + Zip File Upload Write

Fuzzing the website shows that there `/admin` endpoint. Need an admin account to access it.
The login can be bypassed using SQL Injection to get the admin account with `admin' or '1'='1` on both `username` and `password` fields.

Accessing the admin panel shows that there is Bulk upload feature that only accept a zip file.

I try uploading a symlink zip file but it fails.

I try other technique from [Hacktricks](https://book.hacktricks.xyz/pentesting-web/file-upload#zip-tar-file-automatically-decompressed-upload) and it works.

Just follow the steps in the Hacktricks book, the flag can be found at `/var/www/flag.txt`.
