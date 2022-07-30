'''Client:

  After you run the server,
  use command line "client.py localhost portnumber index.htm" to run the client.
  
  You can not run the client by IDLE(Python GUI).
'''

from socket import *
import sys

clientsocket = socket(AF_INET, SOCK_STREAM)

if len(sys.argv) != 4:
    print (len(sys.argv))
    print("Your command is not right. Please be in this format:client.py server_host server_port filename")
    sys.exit(0)

host = str(sys.argv[1])
port = int(sys.argv[2])
request = str(sys.argv[3])
request = "GET /" + request + " HTTP/1.1"
try:
    clientsocket.connect((host,port))
except Exception as data:
    print (Exception,":",data)
    print ("Please try again.\r\n")
    sys.exit(0)
clientsocket.send(request.encode())
    
response = clientsocket.recv(1024)
    
print (response)
    
clientsocket.close()

host = ''

while True:

 clientsocket = socket(AF_INET, SOCK_STREAM)

 host = input("Input Host Address:")

 port = int(input("Input Port Number:"))

 request = input("Input Requested Filename:")

 request = "GET /" + request + " HTTP/1.1"

 try:
  clientsocket.connect((host,port))

 except Exception as data:
  print (Exception,":",data)
  print ("Please try again.\r\n")
  continue
        
 clientsocket.send(request.encode())
    
 response = clientsocket.recv(1024)
    
 print (response)
    
 clientsocket.close()
