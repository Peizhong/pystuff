from socket import *

BUFFSIZE=2048

def StartClient(host:str, port:int):
    client = socket(AF_INET,SOCK_STREAM)
    client.connect((host,port))
    while True:
        data = input(">")
        if not data:
            break
        client.send(data.encode())
        data = client.recv(BUFFSIZE).decode()
        if not data:
            break
        print(data)

if __name__ == "__main__":
    StartClient("localhost",8080)