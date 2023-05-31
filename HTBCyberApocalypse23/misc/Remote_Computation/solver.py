import socket, operator, time, re

def calculate(expression):
    match = re.match(r'^\[\d+\]:\s*((?:\d+(?:\.\d+)?(?:\s*[\+\-\*/]\s*\d+(?:\.\d+)?)*))\s*=\s*\?$', expression)
    if not match:
        return "SYNTAX_ERR"
    else:
        try:
            result = eval(match.group(1))
            if result < -1337.00 or result > 1337.00:
                return "MEM_ERR"
            else:
                return format(result, '.2f')
        except ZeroDivisionError:
            return "DIV0_ERR"

host = "144.126.196.198"
port = 30940
result = 0

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host, port))

res = s.recv(1024)

print(res)
time.sleep(1)
s.send(b'1\n')
s.recv(38)
while True:
    lines = s.recv(1024)
    if b'HTB' in lines:
        print(lines)
        break
    else:
        expression = lines[:-2].decode()
        print(expression)
        result = calculate(expression)

        print(bytes(str(result),'utf-8'))
        s.send(bytes(str(result)+'\n','utf-8'))
