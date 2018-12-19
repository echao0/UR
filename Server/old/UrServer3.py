import socket
import sys

import time
from thread import *
import SocketServer
import argparse  # biblioteca para argumentos

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action="store_true")
python_args = parser.parse_args()


class miserver():
    global server_on
    global python_args
    global python_args

    def __init__(empty):
        if python_args.verbose:
            print "La clase", "esta iniciada"

    def start(self):

        t = threading.Thread(target=self.server_start)  # Creo el hilo para la escucha de puerto
        t.start()  # Inicio el hilo de la escucha de puerto
        if python_args.verbose:
            print "Servidor iniciado y a la espera"

    def server_start(self):  # Funcion de inicio y control de puerto de escucha
        try:
            server = SocketServer.TCPServer((server_host, server_port), ServerHandler)  # Creo el objeto servidor
            server.socket.settimeout(
                3.0)  # Selecciono un timeout del servidor de 5 segundos (evito fallo de cierre de server)

            while server_on:  # Control de variable de cierre de hilo principal
                server.handle_request()
            else:
                server.socket.shutdown()
                server.socket.close()


        except:
            # print "##### NO ES POSIBLE INICIAR EL SERVER #####"
            # print "      ##### Espero 30 segundos #####"
            time.sleep(30)
            self.server_start()

    def server_start2(self):
        server = SocketServer.TCPServer((server_host, server_port), ServerHandler)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

class ServerHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        self.jump = False
        self.data = self.request.recv(1024).strip()

        if self.data == "beat":  # Control para no imprimir en pantalla latidos
            self.request.send(str("ack"))

def tempo():          #Funcion que se repite durante un tiempo determinado
    while True:
        time.sleep(tempoTime)
        print "temporizador acabado"


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servidor1 = miserver()
servidor1.start()  # Server start to recive packets

while True:
    if not tempoOn:
        tempoOn = True
        start_new_thread(tempo, ())