import socket
import errno

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
# get username
my_username = input("Username: ")

# Create TCP/IPv4 socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect server
client_socket.connect((IP, PORT))

# Set connection to non-blocking state,
client_socket.setblocking(False)

# Create username+message
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)
while True:

    # User input
    message = input(f'{my_username} > ')

    # if there is a message send
    if message:

        # convert message to bytes and send
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)

    try:
        # Other users message
        # Cant get messages until send message(user input blocking)
        while True:

            # Receive our "header" containing username length, it's size is defined and constant
            username_header = client_socket.recv(HEADER_LENGTH)

            # Eğer mesaj alınmıyor ise server kapanmıştır
            if not len(username_header):
                print('Connection closed by the server')
                client_socket.close()

            # Convert header to int value
            username_length = int(username_header.decode('utf-8').strip())

            # get username and convert it from byte to sting
            username = client_socket.recv(username_length).decode('utf-8')

            # get username and convert it from byte to sting
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            print(f'{username} > {message}')

    except IOError as e:
        #Errors
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            client_socket.close()
        continue

    except Exception as e:
        # Diğer durumlar
        print('Reading error: '.format(str(e)))
        client_socket.close()