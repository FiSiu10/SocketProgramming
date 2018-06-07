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
if b'READY' in ready:
    state = 1       
    while state != 4:
        if state == 1:
            s1.sendall(b'GET '+ bytearray(part.path, 'UTF-8') + b' HTTP/1.1\n'
                +b'User-Agent: curl/7.16.3 libcurl/7.16.3 OpenSSL/0.9.7l zlib/1.2.3\n'
                +b'Host: webhost\n'
                +b'Accept-Language: en\n\n') 
            reply = s1.recv(1024)
            s = reply.decode("UTF-8")
            if '<HTML>' in s:
                i = s.index("<HTML>")
                state = 2
        if state == 2:
        	#q = s2.sendall(s[i:].encode("UTF-8"))
        	if '</HTML>' in s:
        		if '<HTML>' in s:
        			i2 = s.index("</HTML>")
        			send = s[i:i2]
        			s2.sendall(send.encode("UTF-8"))
        			state = 3
        	else:
        		s2.sendall(s[i:].encode("UTF-8"))
        		#s = s1.recv(1024).decode("UTF-8")
        if state == 3:
            reply2 = s2.recv(1024)
            r = reply2.decode("UTF-8")
            convert = 'ICS 200 HTML CONVERT COMPLETE'
            if convert in r:
                p = r.index(convert)
                print (r[:p], end="")
                state = 4
            else:
            	state = 3
            	print (r, end="")
                    	

    s1.close()
    s2.close()

