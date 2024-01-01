# Solution

Identify the possibly operating system.
```bash
volatility2 -f memory.raw imageinfo
```

I gonna pick the first suggested profile and identify the commandline history.
```bash
volatility2 -f memory.raw --profile=Win7SP1x64 consoles
```

The flag file is `flag.txt` so the encrypted file is `flag.txt.enc`. When encrypting a file using `sussy.exe`, there will be a key generated in the same directory named `key.bin`.
I gonna see in which offset for the two files.
```bash
volatility2 -f memory.raw --profile=Win7SP1x64 filescan | grep -e flag.txt.enc -e key.bin
```

Then I will dump those files.
```bash
mkdir files_dump
volatility2 -f memory.raw --profile=Win7SP1x64 dumpfiles -Q 0x000000001e52b2d0 --name file -D files_dump
volatility2 -f memory.raw --profile=Win7SP1x64 dumpfiles -Q 0x000000001fa97c50 --name file -D files_dump
```

I noticed that the file size is rather large and there are many null bytes in the file. The `flag.txt.enc` file has null bytes in the middle of the data, so I can't remove the null bytes right away. For `key.bin` the null bytes are only present after the data, so I can remove the null bytes right away.

```bash
tr < file.None.0xfffffa800872a5a0.key.bin.dat -d '\000' > key.bin
```

For the `flag.txt.enc` file, I will change the null bytes in the middle of the data to `0x11` using a Hex Editor and change it to null bytes again after removing the null bytes.
```bash
tr < file.None.0xfffffa80084130a0.flag.txt.enc.dat -d '\000' > flag.txt.enc
```

Then, copy `sussy.exe` to the `files_dump` directory and decrypt the `flag.txt.enc` file.
```bash
cp ../sussy.exe 
wine sussy.exe -d flag.txt.enc
```

The flag should be inside `flag.txt.enc.dec` file.
