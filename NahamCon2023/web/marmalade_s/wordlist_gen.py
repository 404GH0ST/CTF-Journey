import string
alpha = string.ascii_lowercase
fp = open("wordlist.txt", "w")
preced = open("secret_preced", "r").read()
for i in alpha:
  for j in alpha:
    for k in alpha:
      for l in alpha:
          for m in alpha:
            fp.write(preced.strip() + str(i) + str(j) + str(k) + str(l) + str(m) + "\n");

fp.close()
