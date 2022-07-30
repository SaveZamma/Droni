import socket
import threading
import sys
import time

class Client(threading.Thread): # L'oggetto Client è di tipo thread cosicchè possa convivere simultaneamente con il server
    def __init__(self, chatApp): # Initializza con un riferimento la App della Chat
        super(Client, self).__init__()
        self.chatApp = chatApp
        self.isConnected = False # Stato della Connessione

    # Inizializza il metodo chiamato dal modulo threading
    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Crea un nuovo socket
        self.socket.settimeout(5)

    def conn(self, args):
        if self.chatApp.nickname == "": # Controlla se il nickname è impostato e restituisce False in caso negativo
            self.chatApp.sysMsg(self.chatApp.lang['nickNotSet'])
            return False
        host = args[0] # IP del peer
        port = int(args[1]) # Porta del peer
        self.chatApp.sysMsg(self.chatApp.lang['connectingToPeer'].format(host, port))
        try: # Tenta di connettersi e cattura eventuali errori in caso di fallimento
            self.socket.connect((host, port))
        except socket.error:
            self.chatApp.sysMsg(self.chatApp.lang['failedConnectingTimeout'])
            return False
        self.socket.send("\b/init {0} {1} {2}".format(self.chatApp.nickname, self.chatApp.hostname, self.chatApp.port).encode()) # Exchange initial information (nickname, ip, port)
        self.chatApp.sysMsg(self.chatApp.lang['connected'])
        self.isConnected = True # Imposta lo stato della connessione in stato true
    
    # Metodo chiamato dalla app della Chat per resettare il socket del client
    def stop(self):
        self.socket.close()
        self.socket = None

    # Metodo per inviare i dati ad un peer
    def send(self, msg):
        if msg != '':
            try:
                self.socket.send(msg.encode())
                return True
            except socket.error as error:
                self.chatApp.sysMsg(self.chatApp.lang['failedSentData'])
                self.chatApp.sysMsg(error)
                self.isConnected = False
                return False


    


