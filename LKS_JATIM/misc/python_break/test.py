
def check(usr_input):
    ll = [inp.isalpha() for inp in usr_input]
    print(ll)
    if sum(ll) > 0:
            print("Banned!")
            exit(-1337)
    else:
            try:
                    os.system(usr_inp)
            except Exception as e:
                    print("Wah untung masih ketahuan satpam. Kamu tetap di banned!")
                    exit(-1)

while True:
    inp = input("Command: ")
    check(inp)

