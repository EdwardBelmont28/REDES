#!/usr/bin/env python3
from time import time
from Tablero import *
import socket
#HOST=input("Bienvenido a BUSCAMINAS\nIngresa el ip del Servidor: ")
#PORT=input("\nIngresa el puerto del servidor: ")
HOST = "192.168.100.100"
PORT = 54321
bufferSize = 1024
UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
UDPClientSocket.connect((HOST, PORT))
print("Conectado al Servidor!")

Dificultad=input ("\nEscoge la dificultad del juego: \n1.Facil\n2.Dificil.\n\nIngresa la dificultad: ")
UDPClientSocket.send(Dificultad.encode('utf-8'))
Buscaminas=Tablero(int(Dificultad),0)
tiempo_inicial = time()
print("\n\nBienvenido a BUSCAMINAS\n\n")
while Buscaminas.Estado==1:
          print()
          print()
          Buscaminas.imprimir()
          XY = input("\nIngresa las cordenadas de la casilla que quieres destapar: (X Y):  ")
          X, Y = XY.split(' ')
          UDPClientSocket.send(X.encode('utf-8'))
          UDPClientSocket.send(Y.encode('utf-8'))
          Respuesta = UDPClientSocket.recv(bufferSize)
          if int(Respuesta) == 1:
                  Buscaminas.Estado = 0
                  Buscaminas.destaparM(int(XY[0]), int(XY[2]))
                  Buscaminas.Ganador == 0
          elif int(Respuesta) == 0:
                  Buscaminas.destapar(int(XY[0]), int(XY[2]))
                  Buscaminas.abiertas += 1
                  if Buscaminas.libres == Buscaminas.abiertas:
                      Buscaminas.Estado = 0
                      Buscaminas.destaparM(int(XY[0]), int(XY[2]))
                      Buscaminas.Ganador == 1



tiempo_final = time()
print("\n\nJuego Terminado\n\n")
Buscaminas.imprimir()
if Buscaminas.Ganador==1:
    print("\nHas Ganado!!! UwU")
else:
    print("\nPerdiste Crack!  :'C")
tiempo_ejecucion = tiempo_final - tiempo_inicial
print ("El tiempo jugado fue: ",tiempo_ejecucion)
print("\n\n")
UDPClientSocket.close()