import socket
import signal
import re
import sys
import subprocess

host = ''
port = 80
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(1) # don't queue up any requests


while True:
    csock = None
    caddr = None
    def exit_graceful(signal, frame):
        print('You pressed Ctrl+C!')
        sock.shutdown(socket.SHUT_WR)
        sock.close()
        sys.exit(0)
    signal.signal(signal.SIGINT, exit_graceful)
    signal.signal(signal.SIGTERM, exit_graceful)
    signal.signal(signal.SIGHUP, exit_graceful)
    signal.signal(signal.SIGHUP, exit_graceful)
    signal.signal(signal.SIGABRT, exit_graceful)
	
    csock, cadds = sock.accept()
    req = csock.recv(1024) # get the request, 1kB max
    match = re.match('GET /request-certs', req)
    if match:
        subprocess.call(['./root/renewAndSendToProxy.sh'])
        csock.sendall("""HTTP/1.0 200 OK
Content-Type: text/html

<html>
<head>
<title>Success</title>
</head>
<body>
Certs renewed and send to proxy!
</body>
</html>
""")
    else:
        # If there was no recognised command then return a 404 (page not found)
        csock.sendall("HTTP/1.0 404 Not Found\r\n")
    csock.close()
