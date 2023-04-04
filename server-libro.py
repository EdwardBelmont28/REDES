import socket
import select

HOST = 'localhost'
PORT = 65432
BUFFER_SIZE = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print('El servidor disponible y esperando solicitudes')
#Lista de sockets
    sockets_lista = [server_socket]

    while True:
        read_sockets = select.select(sockets_lista, [], [])
        for socket in read_sockets:
            if socket == server_socket:
                client_socket, client_addr = server_socket.accept()
                sockets_lista.append(client_socket)
                print('Cliente conectado:', client_addr)
            else:
                if data:
                    print('Recibiendo del cliente', socket.name(), ':', data.decode())
                else:
                    socket.close()
                    sockets_lista.remove(socket)
