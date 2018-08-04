import socket
from multiprocessing import Process
from threading import Thread
import time
import os

HOST = 'localhost'
PORT = 4343


def hello():
    print('this is a process ', os.getpid())


def start_client(host, port):
    print('client waiting for server {}:{} start up'.format(host, port))
    time.sleep(1)
    print('client let\'s go')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    print('client connected')
    while True:
        data = s.recv(1024).decode()
        if data == 'close':
            break
        print('recived:', data)
    s.close()


def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    print('waiting for connection')
    s.listen()
    conn, addr = s.accept()
    print('client {} accepted at {}'.format(addr, time.time()))
    message = 'hello'
    conn.send(message.encode())
    while True:
        message = input('say something:')
        if not message:
            break
        conn.send(message.encode())
    conn.close()


if __name__ == '__main__':
    server_thread = Thread(target=start_server)
    server_thread.start()
    p = Process(target=start_client, args=(HOST, PORT))
    p.start()
    server_thread.join()
    print('over')
