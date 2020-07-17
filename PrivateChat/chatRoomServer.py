import socket
import select

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234

#Create TCP/IPv4 Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Set REUSEADDR
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#server
server_address = (IP, PORT)
# Bind server with ıp/port
server_socket.bind(server_address)
# Wait connections
server_socket.listen()

# Soket List
sockets_list = [server_socket]

# Connected Soket List
clients = {}

print(f'Listening for connections on {IP}:{PORT}...')

# receive message func
def receive_message(client_socket):

    try:

        # get message 
        message_header = client_socket.recv(HEADER_LENGTH)

        # if there isnt a message
        if not len(message_header):
            return False

        # set message length
        message_length = int(message_header.decode('utf-8').strip())

        # return message as a object
        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:
        # Diğer durumlar için false döndür 
        return False

while True:

    #  Unix select() yada Windows select() WinSock 3 parametre ile çağır:
    #   - rlist - gelen mesajın izleneceği soketler
    #   - wlist - mesaj gönderilecek soketler
    #   - xlist - hata veren soketler
    # Returns lists:
    #   - reading - mesaj aldığımız soketler
    #   - writing - mesaj almaya uygun soketler
    #   - errors  - diğer durumdaki soketler
    # aynı zamanda soketlerin birbirini bloklamasını engeller
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)


    # For each socket in Socket List
    for notified_socket in read_sockets:

        # New connection
        if notified_socket == server_socket:

            # Accepted connection
            client_socket, client_address = server_socket.accept()

            # Client 
            user = receive_message(client_socket)

            #
            if user is False:
                continue
            #dont allow users have same name
            i=0
            for elem in clients.keys():
                tmp=clients[elem]
                if tmp['data']==user['data']:
                    print( "username taken")
                else:
                    i=i+1
            #accept connection
            if(i==len(clients)):
                print("yeni olustur")
                # Add in  select.select() list
                sockets_list.append(client_socket)
                # Client
                clients[client_socket] = user
                print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))

        # Existed socket 
        else:

            # Get message
            message = receive_message(notified_socket)

            # 
            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))

                # delete socket.socket() list
                sockets_list.remove(notified_socket)

                # remove Client list
                del clients[notified_socket]

                continue

            # Check who is sending
            user = clients[notified_socket]

            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
            #Sending possibilities
            target=""            
            tmp=message["data"].decode("utf-8").split('>')
            # if doesnt target didnt defined with  '>' tmp is single string
            if len(tmp)>1:
                target=tmp[0]
            # Send  clients or target client message
            for client_socket in clients.keys():
                cltTmp=clients[client_socket]
                # clients or target 
                if cltTmp['data'].decode('utf-8') == target:
                    print("broadcasting to: ", cltTmp['data'].decode('utf-8'))
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
                elif client_socket != notified_socket and target=="":
                   # print("broadcasting to: ", cltTmp['data'].decode('utf-8'))
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    # Hatalı(exepction) soketleri kaldır
    for notified_socket in exception_sockets:

        # socket.socket() listesinden kaldır
        sockets_list.remove(notified_socket)

        # clientlardna kaldır
        del clients[notified_socket]
