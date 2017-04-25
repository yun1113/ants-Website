import socket, sys
import time
import json
from thread import *


# watchdog thread
def threadWork(client):
    global client_socket
    while True:
        msg = client.recv(4096)
        if not msg:
            pass
        else:
            print(msg)
            print("======================================================")
            d = json.loads(msg)
            hash_value = d.get('sample_hash', '')
            print(hash_value)
            if client_socket and hash_value in client_socket.keys():
                for csocket in client_socket[hash_value]:
                    try:
                        csocket.sendall(msg)
                    except socket.error as e:
                        client_socket[hash_value].remove(csocket)
    client.close()

# ========================== Socket initial ==========================
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    sys.stderr.write("[ERROR] %s\n" % msg[1])
    sys.exit(1)

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # reuse tcp
csock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

# ========================== Temu Client ==========================
sock.bind(('140.112.107.39', 10001))

sock.listen(5)
print("server on")

client_socket = {}

while True:
    (csock, adr) = sock.accept()
    print "Client Info: ", csock, adr
    if adr[0].split(".")[0] in ['10', '172', '192']:
        start_new_thread(threadWork, (csock,))
        continue
    else:
        msg = csock.recv(4096)
        if msg not in client_socket.keys():
            client_socket[msg] = []
        client_socket[msg].append(csock)
        # print(client_socket[msg])
    