import socket
import time
import pickle

SERVER_ADDR = '2804:d51:5001:8300:3d13:405b:291b:20f' #'192.168.100.8' #socket.gethostname()
PORT = 1255


my_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
my_socket.bind((SERVER_ADDR, PORT))
my_socket.listen(2)

con, address = my_socket.accept()
con.close()

sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)


time.sleep(1)

for i in range(1000):
    # time.sleep(0.5)
    sock.sendto(pickle.dumps(i), (SERVER_ADDR, PORT))
    
sock.sendto(pickle.dumps("!END"), (SERVER_ADDR, PORT))
