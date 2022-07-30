'''Corso di Programmazione di Reti - Esercitazione 7'''

import socket, threading
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 1911))
s.listen(1)
 
lock = threading.Lock()
 
welcome_message = '\r\nBenvenuto su Telnet Server\r\n\r\nOpzioni Disponibili\r\n\r\n1. Restituisce la Lista delle Directory\r\n2. Restituisce la Directory corrente\r\n3. Esci\r\n'
 


class daemon(threading.Thread):
    def __init__(self, a):
        threading.Thread.__init__(self)
        self.socket = a[0]
        self.address = a[1]
    def run(self):
        # visualizza il welcome message
        self.socket.send(welcome_message.encode())
        while(True):
            data = self.socket.recv(1024).decode()
            print(data)
            # gestisce le alternative del menu e restituisce il messaggio di riferimento
            if data[0] == '1':
                # eseguiamo la funzione di listare le directory contenute nella directory corrente
                data = '\r\n'+str(os.listdir())+'\r\n'
            elif data[0] == '2':
                data = '\r\n'+str(os.getcwdb())+'\r\n'
                # eseguiamo la funzione di Exit
            elif data[0] == '3':
                break;
            else:
                data = welcome_message
            # restituisce il messaggio di benvenuto al client
            self.socket.send(data.encode());
        # chiude la connessione
        self.socket.close()
     
while True:
    daemon(s.accept()).start()

