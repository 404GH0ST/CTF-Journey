# Solution

Extract the squashfs file `content` directory.
```bash
unsquashfs -d content secure_router.bin
```

Get the timezone at `content/etc/timezone`

Read the source code in the `content/var/www/` directory.

According to the source, it only needs a correct timestamp to recover the credential.

I have created a solve script to get the flag.
