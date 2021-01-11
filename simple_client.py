import socket
import time
import pickle
from datetime import datetime

SERVER_ADDR = '2804:d51:5001:8300:3d13:405b:291b:20f' #'192.168.100.8' #socket.gethostname()
PORT = 1255


sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
sock.connect((SERVER_ADDR,PORT))

sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
sock.bind((SERVER_ADDR, PORT))


msg = ''
time = datetime.now().timestamp()
while(msg != '!END'):
    newTime = datetime.now().timestamp()
    print(newTime - time)
    time = newTime
    data, addr = sock.recvfrom(1024)
    msg = pickle.loads(data)
    print(msg)