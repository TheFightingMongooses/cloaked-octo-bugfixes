import socket

UDP_IP = "10.28.27.16"
UDP_PORT = 61556

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", UDP_PORT))

while True:
	data, addr = sock.recvfrom(1024)
	print "received message:", data