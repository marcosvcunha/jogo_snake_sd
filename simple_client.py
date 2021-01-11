import socket
import time
import pickle

SERVER_ADDR = '2804:d51:5001:8300:3d13:405b:291b:20f' #'192.168.100.8' #socket.gethostname()
PORT = 1234


socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
socket.connect((SERVER_ADDR,PORT))

msg = ''

while(msg != '!END'):
    msg = pickle.loads(socket.recv(1024))
    print(msg)
