import threading
#https://stackoverflow.com/a/57387909
#async keyboard input
my_username = input("Username: ")

class KeyboardThread(threading.Thread):

    def __init__(self, input_cbk = None, name='keyboard-input-thread'):
        self.input_cbk = input_cbk
        super(KeyboardThread, self).__init__(name=name)
        self.start()

    def run(self):
        while True:
            self.input_cbk(input()) #waits to get input + Return

showcounter = 0 #something to demonstrate the change

def my_callback(inp):
    message= my_username +">"+inp
    print('gönderilen:', message, ' Counter is at:', showcounter)

#start the Keyboard thread
kthread = KeyboardThread(my_callback)

while True:
    #the normal program executes without blocking. here just counting up
    showcounter += 1