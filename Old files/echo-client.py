#!/usr/bin/env python3

import socket
import sys
import time

BUFSIZE = 1024

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
#server_address = ('localhost', 10000)
server_address = (sys.argv[1], 10000)

# Get message content
#content = sys.arg[2]

print >> sys.stderr, 'connecting to %s port %s' % server_address

sock.connect(server_address)

# try:

# Send data
#message = 'This is the message.  It will be repeated.'
#message = open(content, 'r').read()
message = 'ppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppT'

print >> sys.stderr, 'sending "%s"' % message
print >> sys.stderr, 'message size in bytes', len(message)

# Wait user input to start sending
# raw_input()

while True:
	
	sock.send(message)
	
	# Look for the response
	amount_received = 0
	amount_expected = len(message)
	
	while amount_received < amount_expected:
		data = sock.recv(1024)
		amount_received += len(data)
		#print >> sys.stderr, 'received "%s"' % data
		print >> sys.stderr, 'received ', amount_received
		
	print >> sys.stderr, 'sending message again...'
	time.sleep(3)

# finally:
#     print >>sys.stderr, 'closing socket'
#     sock.close()
