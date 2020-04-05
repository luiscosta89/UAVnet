from __future__ import print_function

import datetime
import socket

HOST = '127.0.0.1'
PORT = 50000
BUFFER = 4096

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST,PORT))
sock.listen(0)
print('listening at %s:%s\n\r' %(HOST, PORT))

while True:
    client_sock, client_addr = sock.accept()

    starttime = datetime.datetime.now()
    print(starttime, end="")
    print('%s:%s connected\n\r' % client_addr)

    count = 0
    while True:
        data = client_sock.recv(BUFFER)
        if data:
            count += len(data)
            del data
            continue

        client_sock.close()

        endtime = datetime.datetime.now()
        print(endtime)
        print('%s:%s disconnected\n\r' % client_addr)

        print('bytes transferred: %d' % count)
        delta = endtime - starttime
        delta = delta.seconds + delta.microseconds / 1000000.0
        print('time used (seconds): %f' % delta)
        print('averaged speed (MB/s): %f\n\r' % (count / 1024 / 1024 / delta))
        break

sock.close()
