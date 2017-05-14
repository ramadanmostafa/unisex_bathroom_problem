"""
Simple client that connects to the socket server request enter the bathroom
send male to the socket server
"""
import socket
import time

# ip address of the server
HOST = '127.0.0.1'

# port number that the socket server is listening to
PORT = 8888

# initiate the soket client
soket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soket_client.connect((HOST, PORT))

# send a message to the socket server "male"
soket_client.sendall('male')
while True:
    time.sleep(2)
    soket_client.sendall('am i done?')
    data = soket_client.recv(1024)
    print 'Received', repr(data)

# close the soket client
soket_client.close()
