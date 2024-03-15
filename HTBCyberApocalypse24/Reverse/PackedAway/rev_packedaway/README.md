# Solver
We could see `upx` signature by running `strings` on the binary, so we can unpack this binary using `upx -d`
```
upx -d packed
```

Run `strings packed | grep HTB` to get the flag
