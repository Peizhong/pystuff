import socket
import sys
sys.path.append("..")
import myutils

@myutils.clock
def tcpboom():
    for i in range(30000):
        s = socket.socket()
        s.connect(("localhost",5000))
        msg = "hello %s"%i
        s.send(msg.encode('utf-8'))
        s.recv(1024)
        s.close()
    
tcpboom()