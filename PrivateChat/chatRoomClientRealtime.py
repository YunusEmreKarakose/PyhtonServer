import socket
import errno
import threading
from os import system, name 
import sys   
# clear console
def clearConsole(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 
  
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
# clientın yapabileceği işlemler
def clientOps(keyboardInput):
    condition=""
    tmp=keyboardInput.split('>')
    # eğer > ibaresi ile bir hedef gösterilmemişse tmp sadece bir string içerir
    if len(tmp)>1:
        condition=tmp[0]
    #Durumlar
    #1. Özel bir konuşma
    if condition=="conversation":
        #bu durumda tmp[1] konuşma yapılan kişiyi belirtir (conservation>name)
        print("conversation",tmp[1])
        #all chat
        if tmp[1]=="all":
            clearConsole()
            print("Client: "+my_username)
            filename    =   my_username+"&all.txt"
            fileptr =open(filename,"r")
            print(fileptr.readline())
            lines=fileptr.readlines()
            for line in lines:
                print(line)
            fileptr.close()
        else:
            clearConsole()
            print("Client: "+my_username)
            filename    =   my_username+"&"+tmp[1]+".txt"
            fileptr =open(filename,"r")            
            lines=fileptr.readlines()
            for line in lines:
                print(line)
            fileptr.close()

    #mesaj yollamak
    else:
        #
        message = keyboardInput
        # Mesaj boş değilse yolla
        if message:

            # Mesajı göndermek için byte haline getir ve yolla
            message = message.encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(message_header + message)
            #Yollanan mesajı kaydet
            #mesajı bytedan stringe geri çevir            
            message = message.decode('utf-8')
            target=""            
            tmp=message.split('>')
            # eğer > ibaresi ile bir hedef gösterilmemişse tmp sadece bir string içerir
            if len(tmp)>1:
                target=tmp[0]
            #konuşmayı client tarafında sakla
            #özel mesaj ise ayrı bir dosyada sakla
            if target!="":
                filename    =   my_username+"&"+target+".txt"
                fileptr =open(filename,"a+")
                fileptr.write(my_username+">"+target+">"+message+"\n")
                fileptr.close()
            #herkese açık mesajları sakla
            else:
                filename    =   my_username+"&all.txt"
                fileptr =open(filename,"a+")
                fileptr.write(my_username+">"+message+"\n")
                fileptr.close()


#start the Keyboard thread
kthread = KeyboardThread(clientOps)
while True:
    
    

    try:
        # Diğer kullanıcıları servera yolladığı mesajları alma
        while True:

            #
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
            #Mesaj clienta özelmi gönderildi?
            target=""            
            tmp=message.split('>')
            # eğer > ibaresi ile bir hedef gösterilmemişse tmp sadece bir string içerir
            if len(tmp)>1:
                target=tmp[0]
            #konuşmayı client tarafında sakla
            #özel mesaj ise ayrı bir dosyada sakla
            if target!="":
                filename    =   my_username+"&"+username+".txt"
                fileptr =open(filename,"a+")
                fileptr.write(username+">"+message+"\n")
                fileptr.close()
            #herkese açık mesajları sakla
            else:
                filename    =   my_username+"&all.txt"
                fileptr =open(filename,"a+")
                fileptr.write(username+">"+message+"\n")
                fileptr.close()
            #
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