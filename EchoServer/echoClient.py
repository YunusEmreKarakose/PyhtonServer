import socket

# Create TCP/IpV4 socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server
server_address = ('localhost', 3000)
print("Echo Servera Bağlanılıyor: %s:%d" % server_address)

try:
    sock.connect(server_address)
    msg=input("client>")
    while msg != 'exit':
        sock.sendall(msg.encode('utf-8'))
        data = sock.recv(100)
        print('Cevap: %s' %data.decode('utf-8'))
        msg= input('client> ')
except socket.gaierror as err:
    print("Socket Hatası: %s" %str(err))
except Exception as e:
    print(e)
finally:
    sock.close()
