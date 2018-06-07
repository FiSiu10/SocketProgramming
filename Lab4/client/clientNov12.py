import socket
import sys
import os
import time
import random

#python3 clientNov5.py localhost 10000 GET 5.pdf
#create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverName = sys.argv[1]
portNumber = sys.argv[2]
command = sys.argv[4]
file = sys.argv[5]
number = sys.argv[3]

sock.connect((serverName, int(portNumber)))
print(number + " client connects to server")
ready = sock.recv(1024).decode('UTF-8')
print(number + " client has permission to start - READY received")

if 'READY' in ready.upper():
    time.sleep(random.randint(2,6))
    #print("in READY")
    sock.send(bytearray(command, 'UTF-8') + b' ' + bytearray(file, 'UTF-8'))
    #print("b: client: GET filename")
    #b client: GET filename
    
    if command == 'GET':    
        data = sock.recv(1024)
        new = data.decode('UTF-8') 
        if 'ERROR' in new.upper():
            print ("server error: file" + new[6:])
        else:
            try:
                #d: client: READY
                sock.send('READY'.encode('UTF-8'))

                with open(file, 'wb') as f:
                    n = 0
                    new = "";

                    packet = bytearray(8)
                    sock.recv_into(packet)
                    receive = int.from_bytes(packet, byteorder="big", signed=False)

                    #f: client: OK
                    sock.send('OK'.encode('UTF-8'))
                    print ("client receiving file " + file + " (" + str(receive) + " bytes)")

                    while n < receive:
                        #print(number + ": 5")
                        data = sock.recv(min(receive-n, receive))
                        f.write(data)
                        n += len(data)
                    
                    #print(number + ": 6")
                    data = sock.recv(1024)
                    new = data.decode('UTF-8') 
                    if 'DONE' in new.upper():
                        print (number + " COMPLETE")
                    sock.close()
            except:
                print ("client error: unable to create file " + file)
                sock.close()

    if command == 'PUT':
        if (os.path.exists(file)):
            message = sock.recv(1024)
            #d: client: #bytes
            if 'OK' in message.decode('UTF-8'):
                fileSize = os.path.getsize(file)
                packet = fileSize.to_bytes(8, byteorder="big", signed=False)
                sock.send(packet)
                print ("client sending " + str(fileSize) + " bytes")

            try:
                #sock.send('READY'.encode('UTF-8'))
                f = open(file, 'rb')
                l = f.read(1024)
                message2 = sock.recv(1024)
                #f: client: send bytes
                if 'OK' in message.decode('UTF-8'):
                    while l:
                        sock.send(l)
                        l = f.read(1024)
                        
                    data = sock.recv(1024)
                    new = data.decode('UTF-8')
                    if 'DONE' in new.upper():
                        print ("COMPLETE")
                    sock.close()
            except:
                print("client error: unable to create file " + file)

        else:
            sock.send('ERROR'.encode('UTF-8'))
            print ("client error: " + file + " does not exist")

    if command == 'DEL':
        data = sock.recv(1024)
        new = data.decode('UTF-8') 

        if 'ERROR' in new.upper():
            print ("server error: file" + new[6:])
        else:
            print ("client deleting file " + file)
            data = sock.recv(1024)
            new = data.decode('UTF-8')
        
            if 'DONE' in new.upper():
                print ("COMPLETE")
            sock.close()






