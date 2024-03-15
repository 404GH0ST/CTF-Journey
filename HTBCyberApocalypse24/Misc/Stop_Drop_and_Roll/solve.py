from pwn import *

def send_commands(commands): 
    if "HTB" in "".join(commands):
        log.success(commands)
        return False

    log.info(f"Commands: {commands}")
    answer = ""
    for command in commands:
        answer += scenarios[command] + "-"
    
    log.info(f"Answer: {answer[:-1]}")
    r.sendline(answer[:-1].encode())
    return True
    
if len(sys.argv) != 3:
    log.warn(f"Usage: {sys.argv[0]} HOST PORT")
    exit(1)

r = remote(sys.argv[1], sys.argv[2])

scenarios = {"GORGE": "STOP", "PHREAK": "DROP", "FIRE": "ROLL"}

r.sendline(b"y")
r.recvuntil(b"Let's go!\n")
send_commands(r.recvline().strip().decode().split(", "))

lanjut_kah = True
while lanjut_kah == True:
    r.recvuntil(b"do?")
    lanjut_kah = send_commands(r.recvline().strip().decode().split(", "))

r.interactive()
