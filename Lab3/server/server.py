import socket
import sys
import os
#python3 serverNov5.py 10001 -v
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = sys.argv[1]
sock.bind(("", int(port)))
sock.listen(0)

while True:
    if ('-v' in sys.argv):
        print ("server waiting on port " + sys.argv[1])
    
    client, address = sock.accept()
    ip = client.getsockname()

    if ('-v' in sys.argv):
        print ("server connected to client at " + str(ip[0]) + ":" + sys.argv[1])
    
    #a: server: READY
    client.send('READY'.encode('UTF-8'))

    data = client.recv(1024)
    new = data.decode('UTF-8')
    fileName = new[4:]
    i = 0

    #c: server: OK
    client.send('OK'.encode('UTF-8'))   

    if ('-v' in sys.argv):
        print ("server receiving request: " + new)

     
    if 'GET' in new.upper():
        fileSize = os.path.getsize(fileName)
        packet = fileSize.to_bytes(8, byteorder="big", signed=False)
        #e: server: # bytes
        data = client.recv(1024)
        if 'READY' in data.decode('UTF-8'):
            #g: server: send bytes
            client.send(packet)

        if ('-v' in sys.argv):
            print ("server sending " + str(fileSize) + " bytes")

        data2 = client.recv(1024)
        if 'OK' in data2.decode('UTF-8'):
            try:
                f = open(fileName, 'rb')
                l = f.read(1024)

                while l:
                    client.send(l)
                    l = f.read(1024)

                #h: server: DONE
                client.send('DONE'.encode('UTF-8'))
                f.close()
            except:
                message = "ERROR: " + fileName + " does not exist"
                if ('-v' in sys.argv):
                    print(message)
                client.send(message.encode('UTF-8'))
                client.close()
                continue

    if 'PUT' in new.upper():

        try:
            with open(fileName, 'wb') as f:
                n = 0
                new = "";
                
                packet = bytearray(8)
                client.recv_into(packet)
                receive = int.from_bytes(packet, byteorder="big", signed=False)
                #e: server: OK
                client.send('OK'.encode('UTF-8'))

                if ('-v' in sys.argv):
                    print ("server receiving file " + fileName + " (" + str(receive) + " bytes)")

                while n < receive:
                    data = client.recv(min(receive-n, receive))
                    f.write(data)
                    n += len(data)
                #g: server: DONE
                client.send('DONE'.encode('UTF-8'))
            f.close()
        except:
            message = "ERROR: unable to create " + fileName
            if ('-v' in sys.argv):
                print(message)
            client.send(message.encode('UTF-8'))

    if 'DEL' in new.upper():
        if (os.path.exists(fileName)):
            if ('-v' in sys.argv):
                print("server deleting file " + fileName)

            try:
                os.remove(fileName)
                data = "DONE"
                client.send(data.encode('UTF-8'))
                #c: server: DONE
            except:
                message = "ERROR: unable to delete " + fileName
                if ('-v' in sys.argv):
                    print(message)
                client.send(message.encode('UTF-8'))
        else:
            message = "ERROR: " + fileName + " does not exist"
            if ('-v' in sys.argv):
                print(message)
            client.send(message.encode('UTF-8'))
sock.close()
