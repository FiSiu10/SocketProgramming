import socket
import sys
import os
import collections
import threading
import time

class ClientHandler(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client

    def run(self):
        #a: server: READY
        self.client.send('READY'.encode('UTF-8'))

        data = self.client.recv(1024)
        new = data.decode('UTF-8')
        fileName = new[4:]
        i = 0

        #c: server: OK
        self.client.send('OK'.encode('UTF-8'))   
         
        if 'GET' in new.upper():
            fileSize = os.path.getsize(fileName)
            packet = fileSize.to_bytes(8, byteorder="big", signed=False)

            #e: server: # bytes
            data = self.client.recv(1024)

            if 'READY' in data.decode('UTF-8'):
                #g: server: send bytes
                self.client.send(packet)

            data = self.client.recv(1024)

            if 'OK' in data.decode('UTF-8'):
                try:
                    f = open(fileName, 'rb')
                    l = f.read(1024)

                    while l:
                        self.client.send(l)
                        l = f.read(1024)

                    #h: server: DONE
                    self.client.send('DONE'.encode('UTF-8'))
                    f.close()
                except:
                    message = "ERROR: " + fileName + " does not exist"
                    self.client.send(message.encode('UTF-8'))
                    self.client.close()
       
                
        if 'PUT' in new.upper():
            data = self.client.recv(1024)
            new = data.decode('UTF-8')
            if 'OK' in new.upper():
                try:
                    with open(fileName, 'wb') as f:
                        n = 0
                        new = "";

                        packet = bytearray(8)
                        self.client.recv_into(packet)
                        receive = int.from_bytes(packet, byteorder="big", signed=False)

                        if ('-v' in sys.argv):
                            print ("server receiving file " + fileName + " (" + str(receive) + " bytes)")

                        while n < receive:
                            data = self.client.recv(min(receive-n, receive))
                            f.write(data)
                            n += len(data)
                    
                        self.client.send('DONE'.encode('UTF-8'))
                    f.close()
                except:
                    message = "ERROR: unable to create " + fileName
                    if ('-v' in sys.argv):
                        print(message)
                    self.client.send(message.encode('UTF-8'))

        if 'DEL' in new.upper():
            if (os.path.exists(fileName)):
                if ('-v' in sys.argv):
                    print ("server deleting file " + fileName)
                self.client.send('OK'.encode('UTF-8'))
                try:
                    os.remove(fileName)
                    self.client.send('DONE'.encode('UTF-8'))
                except:
                    message = "ERROR: unable to delete " + fileName
                    if ('-v' in sys.argv):
                        print(message)
                    self.client.send(message.encode('UTF-8'))
            else:
                message = "ERROR: " + fileName + " does not exist"
                if ('-v' in sys.argv):
                    print(message)
                self.client.send(message.encode('UTF-8'))

class Manager(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.q = collections.deque()
        self.running = set()

    def addClient(self, client):
        self.client = client
        self.q.append(client)

    def run(self):
        while True:
            runningLength = len(self.running)
            qLength = len(self.q)

            if (runningLength != 0):
                # Running queue: Look for threads to kick out by temporarily appending to a list
                kick = []
                for t in self.running:
                    if not t.isAlive(): kick.append(t)
                for t in kick:
                    self.running.remove(t)

            # Check the waiting queue
            if (qLength != 0):
                # if full sleep for 1 second and return to top of loop
                print("runningLength " + str(runningLength))
                print("qLength " + str(qLength))
                print("ARGV " + str(sys.argv[2]))
                if (runningLength == sys.argv[2]):
                    print("inside sleep")
                    time.sleep(1)
                # Remove next client from q, start thread and add thread to running set
                else:
                    client = self.q.pop()
                    t = ClientHandler(client)
                    t.start()
                    self.running.add(t)
            # q is empty, wait 1 second and return to top
            else:
                print("q is empty")
                time.sleep(1)

# Socket Setup
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = sys.argv[1]
size = int(sys.argv[2])

sock.bind(("", int(port)))

# Create and start manager thread and is continuously running
s = Manager()
s.start()

# Receives a new client connection and creates a client handler thread but
# does not start it --> hands off waiting thread to the manager class
while True:
    print("size: " + str(size))
    sock.listen(size)
    client, address = sock.accept()
    s.addClient(client)

sock.close()