key1 = "ENO{L1333333333"
key2_chars = [36, 76, 96, 102, 99, 118, 97, 76, 119, 102, 99, 118, 97, 76, 124, 120]
key2 = ''.join(chr(i ^ 19) for i in key2_chars)
key3_chars = "_!ftcnocllunlol_"
key3 = key3_chars[::-1]
key4 = "you_solved_it!!}"

print(f"Flag : {key1+key2+key3+key4}")

