import socket

MAX = 5
# Create TCP/IpV4 socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Reuse same address
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

# server
server_address = ('localhost', 3000)
print("Server Running: %s:%d" % server_address)
# Bind
sock.bind(server_address)
# Max connection
sock.listen(MAX)
# Accepted client
client, address = sock.accept()

while True:
    data = client.recv(100)
    if data:
        print("Message from Client %s" % data.decode('utf-8'))
        answer = "Answer with recived message:::"+str(data.decode('utf-8'));
        client.send(answer.encode('utf-8'))
client.close()