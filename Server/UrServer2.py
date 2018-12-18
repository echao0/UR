import socket
import select
from thread import *
import sys

# -----------------------Change process name to "UrServer"-----------------
import ctypes

libc = ctypes.cdll.LoadLibrary('libc.so.6')
libc.prctl(15, 'UrServer', 0, 0, 0)
# -----------------------------------------------------------------------

import argparse  # biblioteca para argumentos

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action="store_true")
python_args = parser.parse_args()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if python_args.verbose:
    print "Servidor creado he iniciado"


IP_address = '192.168.3.181'
Port = 8000
server.bind((IP_address, Port)) 

server.listen(100)    #listens for 100 active connections. This number can be increased as per convenience
list_of_clients=[]

def clientthread(conn, addr):
    conn.send("Welcome to this chatroom!")
    while True:

            try:     
                message = conn.recv(2048)
                if message:
                    print "<" + addr[0] + "> " + message
                    message_to_send = "<" + addr[0] + "> " + message

                    if (message != "\r"):
                        broadcast(message_to_send,conn)
                        conn.send("ack\r")
                        x = 0
                        for clients in list_of_clients:
                            x = x + 1
                        print "numero total de clientes conectados: " + str(x)

                    #prints the message and address of the user who just sent the message on the server terminal
                else:
                    remove(conn)
            except:
                continue

def broadcast(message,connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message)
            except:
                clients.close()
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

while True:
    conn, addr = server.accept()
    """
    Accepts a connection request and stores two parameters, conn which is a socket object for that user, and addr which contains
    the IP address of the client that just connected
    """
    list_of_clients.append(conn)
    print addr[0] + " connected"
    #maintains a list of clients for ease of broadcasting a message to all available people in the chatroom
    #Prints the address of the person who just connected
    start_new_thread(clientthread,(conn,addr))
    #creates and individual thread for every user that connects


conn.close()
server.close()