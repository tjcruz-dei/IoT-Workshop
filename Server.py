import socket
host = 'localhost'
port = 8888
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()
print(f"Listening on {host}:{port}...")

# 1. aceitar pedidos
# 2. processar
# 3. responder ao cliente

while True:
  client_socket, address = server_socket.accept()
  print(f"Connection from {address[0]}:{address[1]}")
  client_socket.send(b"Hello, world from the server!!")
  client_socket.close()
