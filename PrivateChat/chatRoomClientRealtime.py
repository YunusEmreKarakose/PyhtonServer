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
#Get username
my_username = input("Username: ")

#create TCP/IPv4 socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect server
client_socket.connect((IP, PORT))

# Set connection to non-blocking state, so .recv() call won;t block, 
client_socket.setblocking(False)

# prepage username+message
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)
# operations that clients can do
def clientOps(keyboardInput):
    condition=""
    tmp=keyboardInput.split('>')
    # if doesnt target didnt defined with  '>' tmp is single string
    if len(tmp)>1:
        condition=tmp[0]
    #operations
    #see old messages
    #1. Private Message
    if condition=="conversation":
        #In this case tmp[1] is target (conservation>name)
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

    #Send message
    else:
        #
        message = keyboardInput
        # if there is message send
        if message:

            # convert message to bytes
            message = message.encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(message_header + message)
            #save sending message
            #convert message byte to string           
            message = message.decode('utf-8')
            #store sending messages
            target=""            
            tmp=message.split('>')
            # if doesnt target didnt defined with  '>' tmp is single string
            if len(tmp)>1:
                target=tmp[0]
            #store conversation client tarafında sakla
            #private message
            if target!="":
                filename    =   my_username+"&"+target+".txt"
                fileptr =open(filename,"a+")
                fileptr.write(my_username+">"+target+">"+message+"\n")
                fileptr.close()
            #all chat
            else:
                filename    =   my_username+"&all.txt"
                fileptr =open(filename,"a+")
                fileptr.write(my_username+">"+message+"\n")
                fileptr.close()


#start the Keyboard thread
kthread = KeyboardThread(clientOps)
while True:
    
    

    try:
        # Get message
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