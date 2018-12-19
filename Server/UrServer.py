#!/usr/bin/env python3

import sys
import socket
import selectors
import types

# -----------------------Change process name to "UrServer"-----------------
import threading
import time
import ctypes

libc = ctypes.cdll.LoadLibrary('libc.so.6')
libc.prctl(15, 'UrServer', 0, 0, 0)
# -----------------------------------------------------------------------
working = True #variable para matar al temporizador

NodePassword = 8613
sleep_time = 0.7  # Time to wait in infinite loop (CPU control)
tempoTime = 5

sel = selectors.DefaultSelector()

def tempo():          #Funcion que se repite durante un tiempo determinado
    while working == True:
        time.sleep(tempoTime)
        print("temporizador acabado")
        try:
            for key, mask in events:
                key.data.outb = b'alive\r'
        except:
            pass

def packetHandling(data,key):

        data = data.decode('UTF-8')  # convert to string (Python 3 only)
        data = data.replace("\n", "")  # remove newline character
        data = data.replace("\r", "")  # remove newline character

        if data.count(",") == 1:
            data = data.split(",")
            if data[0] == "name":
                key.name = data[1]

            if data[0] == "alive":
                key.name = data[1]

        else:
            print(data)

        if data == "TestNodeMcu":
            return b'ack_server'

def secure(conn):
    data = "vacio"
    data = conn.recv(1024)  # Should be ready to read
    if data:
        data = data.decode('UTF-8')  # convert to string (Python 3 only)
        data = data.replace("\n", "")  # remove newline character
        data = data.replace("\r", "")  # remove newline character
        try:
            data = int(data)
        except:
            data = 0

        print(data)

        if (data == NodePassword):
            return 1
        else:
            return data


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read

    password = secure(conn)
    if (password == 1):
        print("accepted connection from", addr)
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"", name=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        sel.register(conn, events, data=data)
    else:
        print("Password incorrecto: ", password, "dede la IP: ", addr)
        conn.close()


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            #data.outb += recv_data
            data.outb = packetHandling(recv_data,data)
        else:
            print("closing connection to", data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print("enviando:", repr(data.outb), "to", data.addr, "alias", data.name)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]


if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print("listening on", (host, port))
lsock.setblocking(False)

sel.register(lsock, selectors.EVENT_READ, data=None)

htempo = threading.Thread(target=tempo)
htempo.start()

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
           # print (key.data)
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
        time.sleep(sleep_time)

except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
    working = False
finally:
    sel.close()
