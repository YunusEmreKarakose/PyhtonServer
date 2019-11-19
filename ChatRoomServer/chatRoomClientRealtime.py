import socket
import errno
import threading

class KeyboardThread(threading.Thread):

    def __init__(self, input_cbk = None, name='keyboard-input-thread'):
        self.input_cbk = input_cbk
        super(KeyboardThread, self).__init__(name=name)
        self.start()

    def run(self):
        while True:
            self.input_cbk(input()) #waits to get input + Return



HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
# kullanıcı adını al
my_username = input("Username: ")

# TCP/IPv4 soketi oluştur
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Servera bağlan
client_socket.connect((IP, PORT))

# Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
client_socket.setblocking(False)

# Kullanıcı adını ve mesajı gönderme için hazırla
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)
# mesaj gönderme fonku
def send_message(msg):
    # Kullanıcıdan mesaj almayı bekle
    message = msg

    # Mesaj boş değilse yolla
    if message:

        # Mesajı göndermek için byte haline getir ve yolla
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)


#start the Keyboard thread
kthread = KeyboardThread(send_message)
while True:
    
    

    try:
        # Diğer kullanıcıları servera yolladığı mesajları alma
        while True:

            # Receive our "header" containing username length, it's size is defined and constant
            username_header = client_socket.recv(HEADER_LENGTH)

            # Eğer mesaj alınmıyor ise server kapanmıştır
            if not len(username_header):
                print('Connection closed by the server')
                client_socket.close()

            # Convert header to int value
            username_length = int(username_header.decode('utf-8').strip())

            # Kullanıcı adını al ve bytedan stringe çevir
            username = client_socket.recv(username_length).decode('utf-8')

            # Mesajı al ve bytedan stringe çevir
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            print(f'{username} > {message}')

    except IOError as e:
        #Hata durumları
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            client_socket.close()
        continue

    except Exception as e:
        # Diğer durumlar
        print('Reading error: '.format(str(e)))
        client_socket.close()