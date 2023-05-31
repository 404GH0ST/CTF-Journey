
c = 0

with open("data.dat","r") as f:
    content = f.readlines()
    for line in content:
        if(line.count('0') % 3 == 0) or (line.count('1') % 2 == 0):
            c += 1

print(c)
