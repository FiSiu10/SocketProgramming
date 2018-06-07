import socket
import sys
from urllib.parse import urlparse

#create a socket object
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

o = sys.argv[1]
part = urlparse(sys.argv[1])
webhost = part.netloc

s1.connect((webhost, 80))
s2.connect((webhost, 10010))

ready = s2.recv(1024)
old = '';
old2 = '';
if b'READY' in ready:
    state = 1   

    while state != 4:
        if state == 1:
            s1.sendall(b'GET '+ bytearray(part.path, 'UTF-8') + b' HTTP/1.1\n'
                +b'User-Agent: curl/7.16.3 libcurl/7.16.3 OpenSSL/0.9.7l zlib/1.2.3\n'
                +b'Host: webhost\n'
                +b'Accept-Language: en\n\n') 
            reply = s1.recv(1024)
            new = reply.decode("UTF-8") 
            if '<HTML>' in new.upper():          
                state = 2

        if state == 2:
            if '<HTML>' in new.upper():
                if '</HTML>' in (old.upper() + new.upper()):
                    i = (old + new).index("<HTML>")
                    j = (old + new).index("</HTML>")
                    send = new[i:j] + "</HTML>"
                    state = 3
                else:
                    i = (old + new).index("<HTML>")
                    send = new[i:]
            else:
                if '</HTML>' in (old.upper() + new.upper()):
                    j = (old + new).index("</HTML>")
                    send = new[:j] + "</HTML>"
                    state = 3
                else:
                    send = new[:]
            s2.sendall(send.encode("UTF-8"))
            old = new;
            new = s1.recv(1024).decode("UTF-8")  
            
        if state == 3:
            reply3 = s2.recv(1024)
            new2 = reply3.decode("UTF-8")
            convert = 'ICS 200 HTML CONVERT COMPLETE'
            if convert in (old2.upper() + new2.upper()):
                p = (old2 + new2).index(convert)
                print ((old2 + new2)[:p], end="")
                state = 4
            else:
                state = 3
            old2 = new2;
                
    s1.close()
    s2.close()