import datetime
import socket

HOST = '127.0.0.1'
PORT = 50000
BUFFER = 4096

testdata = b'x' * BUFFER * 4

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST,PORT))
for i in range(1, 1000000):
    sock.send(testdata)
sock.close()
