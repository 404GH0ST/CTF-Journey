
dtmf_data = "67847010810197110123678289808479718265807289125"

for i in range(2, len(dtmf_data)+3, 2):
    print(chr(int(dtmf_data[i-2:i])), end="")
