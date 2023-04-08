import socket
import time

bufferSize = 1024

msgFromServer = "Howdy Client, Happy to be your Server"
ServerPort = 2222
ServerIP = '192.168.43.77'

#Set up socket
bytesToSend=msgFromServer.encode('utf-8')
RPIsocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#When I talk to RPI Socket, I need the IP and the Port. Parameter sent its a tuple
RPIsocket.bind((ServerIP, ServerPort))

print('Server is Up and Listening...')

cnt=0
while True:
    #Sits at this step and pauses until it hears from the client/recieves the message and client address
    message,address=RPIsocket.recvfrom(bufferSize)

    #Decode message recieved
    message=message.decode('utf-8')

    #Print message
    print(message)
    print('Client Address',address[0])
    if message=='INC':
            cnt=cnt+1
    if message=='DEC':
        cnt=cnt-1
    msg=str(cnt)
    msg=msg.encode('utf-8')
    #Send a response back after having recieved the message
    #RPIsocket.sendto(bytesToSend,address)
    RPIsocket.sendto(msg,address)