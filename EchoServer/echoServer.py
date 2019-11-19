import socket

MAX = 5
# Create TCP/IpV4 socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# server
server_address = ('localhost', 3000)
print("Server Calisiyor: %s:%d" % server_address)
# Soketi ilişkilendirme bind()
sock.bind(server_address)
# Maksimum bağlantı sayısı ile dinlemeye başla
sock.listen(MAX)
# Kabul edilen bağlantı
client, address = sock.accept()

while True:
    data = client.recv(100)
    if data:
        print("Clienttan gelen mesaj: %s" % data.decode('utf-8'))
        answer = "Alınan mesajla("+str(data.decode('utf-8'))+ ") verilen cevap "
        client.send(answer.encode('utf-8'))
client.close()