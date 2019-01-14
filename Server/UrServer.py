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

NodePassword = 9
sleep_time = 0.7  # Time to wait in infinite loop (CPU control)
tempoTime = 5
serveName = "Macbook"

host = "192.168.3.181"
port = 1000
sel = selectors.DefaultSelector()

def packetSender(name,data):

    try:
        for key, mask in events:
            dato = key.data.name
            try:
                dato = dato.replace("\n", "")  # remove newline character
                dato = dato.replace("\r", "")  # remove newline character
            except:
                pass

            if dato == name:
                data = data + '\r'
                key.data.outb = bytes(data, 'utf-8')
    except:
        #print ("no se ha encontrado el device")
        pass

def tempo():          #Funcion que se repite durante un tiempo determinado
    #http://www.aprendeaprogramar.com/mod/forum/discuss.php?d=1935
    while working == True:
        time.sleep(tempoTime)
        print("temporizador acabado")
        try:
            for key, mask in events:
                key.data.outb = b'alive\r'
        except:
            pass

def packetHandling(data,key):

        #UrNode2,DeviceOn

        data = data.decode('UTF-8')  # convert to string (Python 3 only)
        data = data.replace("\n", "")  # remove newline character
        data = data.replace("\r", "")  # remove newline character

        #if data.count(",") == 1:
        data = data.split(",")

        if data[0] == "name":
            key.name = data[1]
            return b'name,ok\r\n'

        elif data[0] == "alive":
            key.alive = data[1]
            print (time.strftime("%H:%M:%S"))
            return b'ack\r\n'



        elif data[0] == "urSend":

            if (data[1] == "server"): #Cambio el nombre generico por el especificado en serveName
                data[1] = serveName

            packetSender(data[1], data[2])
            return b'ack_server\r\n'


        else:
            print("recibido general:",data)
            for datos in data:
                print(datos)


        if data == "TestNodeMcu":
            return b'ack_server'

def secure(conn):

    time.sleep(0.1)

    try:
        data = conn.recv(1024)  # Should be ready to read
        print(data)
        if data:
            try:
                data = data.decode('UTF-8')  # convert to string (Python 3 only)
                data = data.replace("\n", "")  # remove newline character
                data = data.replace("\r", "")  # remove newline character
                data = int(data)
            except:
                data = 0

            if (data == NodePassword):
                print("password aceptado:", data)
                return 1
            else:
                return data
    except:
        return 0

def secure_Timer():
    time.sleep(5)
    return 1

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    conn.setblocking(False)

    password = secure(conn)

    if (password == 1):
        print("accepted connection from", addr)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"", name=b"", alive=b"1")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        sel.register(conn, events, data=data)
    else:
        print("Password incorrecto: ", password, "dede la IP: ", addr)
        conn.close()


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    try:
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                #data.outb += recv_data
                data.outb = packetHandling(recv_data,data)
            else:
                print("closing connection to", data.addr, "alias ",data.name)
                sel.unregister(sock)
                sock.close()
    except:
        print("Port died to", data.addr, "alias ", data.name)
        sel.unregister(sock)
        sock.close()
    try:
        if mask & selectors.EVENT_WRITE:
            if data.outb:
               # print("enviando:", repr(data.outb), "to", data.addr, "alias", data.name)
                sent = sock.send(data.outb)  # Should be ready to write
                data.outb = data.outb[sent:]
    except:
        print("2 closing connection to", data.addr, "alias ", data.name)
        sel.unregister(sock)
        sock.close()

"""
if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
"""
def createPort():
    try:
        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lsock.bind((host, port))
        lsock.listen()
        print("listening on", (host, port))
        lsock.setblocking(False)
        sel.register(lsock, selectors.EVENT_READ, data=None)
        return 1

    except:
        return 0

#Bucle de inicio de servidor con tiempo de esper 10 seg
while(True):

    if (createPort() == 1):
        break
    else:
        print( "No es posible crear el servidor, esperando 10 segundos")
        time.sleep(10)


#htempo = threading.Thread(target=tempo)
#htempo.start()

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
