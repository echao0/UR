import socket
import sys

import time
from thread import *
import argparse  # biblioteca para argumentos

# -----------------------Change process name to "UrServer"-----------------
import ctypes

libc = ctypes.cdll.LoadLibrary('libc.so.6')
libc.prctl(15, 'UrServer', 0, 0, 0)
# -----------------------------------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action="store_true")
python_args = parser.parse_args()

HOST = '192.168.3.181'
PORT = 8000
sleep_time = 0.7  # Time to wait in infinite loop (CPU control)

tempoOn = False #Variable para el temporizador de beat
tempoTime = 30
tempoTrigger = False
list_of_clients=[]
NodePassword = 8613

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if python_args.verbose:
    print('# Socket created')

# Create socket on port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('# Bind failed. ')
    s.close()
    sys.exit()

if python_args.verbose:
    print('# Socket bind complete')

s.listen(10)

if python_args.verbose:
    print('# Socket now listening')


def clientthread(conn, addr,clien_num):
    # Receive data from client
    for i in range(1):
        data = conn.recv(1024)


    if (int(data) == NodePassword):
        if python_args.verbose:
            print "password aceptado"

        while True:
                data = conn.recv(1024)
                if data:
                    line = data.decode('UTF-8')  # convert to string (Python 3 only)
                    line = line.replace("\n", "")  # remove newline character
                    serverhandler(line)
                if not data:
                    break
    else:
        conn.close()
        list_of_clients.pop(clien_num)
        if python_args.verbose:
            print "cliente destruido"
            print clien_num

def serverhandler(data):
    if python_args.verbose:
        print "Datos recv:  "
        print data

    if str(data) == "beat\r":  # Control para no imprimir en pantalla latidos
        sender("beat_ok")
    if str(data) == "ack\r":  # Control para no imprimir en pantalla latidos
        sender("mas")

    if str(data) == "UrOn\r":  # Control para no imprimir en pantalla latidos
        sender("DeviceOn")
    if str(data) == "UrOff\r":  # Control para no imprimir en pantalla latidos
        sender("DeviceOff")

def sender(data):
    try:
        for clients in list_of_clients:
            clients.send(str(data) + "\r")
    except:
        pass

def tempo():          #Funcion que se repite durante un tiempo determinado
    while True:
        time.sleep(tempoTime)

        if python_args.verbose:
            print "temporizador acabado"
        try:
            for clients in list_of_clients:
                clients.send("t\r")
        except:
            continue

try:
    while True:

        if (tempoOn == False):
            tempoOn = True
            start_new_thread(tempo,())

        conn, addr = s.accept()

        list_of_clients.append(conn)

        if python_args.verbose:
            print('# Connected to ' + addr[0] + ':' + str(addr[1]))
            print list_of_clients

        valid = len(list_of_clients)-1

        start_new_thread(clientthread,(conn,addr,valid))

        time.sleep(sleep_time)

except KeyboardInterrupt:

    if python_args.verbose:
        print "Detectado el cierre del hilo principal"
        print "Matando hilos secundarios"
    s.close()
    os.system('sudo killall UrServer')





