import socket
import selectors
import time
buffer_size = 32768

sel = selectors.DefaultSelector()
def send_file(filename, sockt):
    with open(filename, 'rb') as file:
        while True:
            data = file.read(buffer_size)
            if not data:
                break
            try:
                sockt.sendall(data)
                time.sleep(0.2)
            except socket.error:
                pass
    print(f"Archivo {filename} enviado con éxito a {sockt.getpeername()}")
    sockt.close()

client_sockets = []
servers = [('localhost', 12345), ('localhost', 56789)]
for server in servers:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setblocking(False)
    client_socket.connect_ex(server)
    sel.register(client_socket, selectors.EVENT_WRITE)
    client_sockets.append(client_socket)
filenames = ['libro.txt']

while client_sockets:
    events = sel.select()
    for key, mask in events:
        if key.fileobj in client_sockets:
            if mask & selectors.EVENT_WRITE:
                send_file(filenames[client_sockets.index(key.fileobj)], key.fileobj)
                sel.unregister(key.fileobj)
                client_sockets.remove(key.fileobj)
print("Archivos enviados con éxito")

for client_socket in client_sockets:
    client_socket.close()
