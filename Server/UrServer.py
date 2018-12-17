#!/usr/bin/env python

# application: [Ur_core]
# version:
# runtime: python
# api_version: 2.7
# autor: echao0
#
# ---Thanks to all the people how share all his knowledge, because they made this things possible!!!
# -------------be curious, be open source, be maker, be open mind and be free!!!
#
#
#
# Use -v to modo vervose

# -----------------------Change process name to "UrServer"-----------------
import ctypes

libc = ctypes.cdll.LoadLibrary('libc.so.6')
libc.prctl(15, 'UrServer', 0, 0, 0)
# -----------------------------------------------------------------------

from socket import *
import SocketServer
import socket

import time  # Se importa para poder leer la hora
import os  # Se importa para poder borrar pantalla de linux
import sys  # Se importa para poder pasar paremetros en la llamada
import datetime  # Para poder consrguir la fecha de ayer
import threading  # Para poder realizar varios Hilos
import argparse  # biblioteca para argumentos

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action="store_true")
python_args = parser.parse_args()


# ------- Configuration Python Server ---------- #
server_host = ''
server_port = int(8000)  # Server socket to comunicate 
server_on = True  # Variable de control de flujo
working = False  # variable para control pila de salida ardu_out

# ------- Time configuration -------#

sleep_time = 0.7  # Time to wait in infinite loop (CPU control)
time_alive = 35  # Time to check if devices are online

class miserver():
    global server_on
    global python_args

    def __init__(empty):
        if python_args.verbose:
            print "La clase Servidor", "esta iniciada"

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

