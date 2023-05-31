import secrets
import socket

def random():
    return secrets.choice([i for i in range(100)])

def main():
    point=0
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('127.0.0.1', 9190)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(server_address)
    server_socket.listen(1)  # Listen for only one client connection

    try:
        print("Waiting for a client to connect...")
        connection, client_address = server_socket.accept()
        print("Client connected:", client_address)
        for _ in range(100):
            ya = False
            server = random()
            for _ in range(7):
                connection.sendall(b"mana?\n")
                client_data = connection.recv(1024)
                client = int(client_data)
                if client != server:
                    if client < server:
                        connection.sendall(b"apah?\n")
                    else:
                        connection.sendall(b"huh?\n")
                else:
                    ya = True
                    connection.sendall(b"good job!\n")
                    break
            if ya:
                point+=1
            else:
                print("good bye!!!")
                break
        if point == 100:
            connection.sendall(b"TCP1P{fakeflag}")
    except Exception as e:
        print("Something went wrong:", str(e))
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
