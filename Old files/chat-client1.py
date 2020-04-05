# Python program to implement client side of chat room. 
import socket 
import select 
import sys 
import time
import random

payload = 'payload.txt'
dummy = 'dummy.txt'

channel_size = 5000000

chunk_size = 1024

message_type = [payload, dummy]

# Create a random function to select the type of file
# And another one to control the size of the chunk
# chunk_payload + chunk_dummy = 5000000

def message_size():
	total_data = 0
	
	while (total_data < channel_size):
		chunk_payload+= chunk_size
		chunk_dumy+= chunk_size
		

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

if len(sys.argv) != 3: 
	print "Correct usage: script, IP address, port number"
	exit() 
IP_address = str(sys.argv[1]) 
Port = int
(sys.argv[2]) 
server.connect((IP_address, Port)) 

while True: 

	# maintains a list of possible input streams 
	sockets_list = [sys.stdin, server] 
	
	selected = random.sample(message_type, 1)
	
	with open(selected, "rb") as file_input:
		while True:
			chunk = file_input.read(chunk_size)

	""" There are two possible input situations. Either the 
	user wants to give manual input to send to other people, 
	or the server is sending a message to be printed on the 
	screen. Select returns from sockets_list, the stream that 
	is reader for input. So for example, if the server wants 
	to send a message, then the if condition will hold true 
	below.If the user wants to send a message, the else 
	condition will evaluate as true"""
	read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 

	for socks in read_sockets: 
		if socks == server: 
			message = socks.recv(2048) 
			print message 
		else:			
			#message = sys.stdin.readline() 			
			message = chunk
			time.sleep(3)
			server.send(message) 
			sys.stdout.write("<You>") 
			sys.stdout.write(message) 
			sys.stdout.flush() 
server.close() 
