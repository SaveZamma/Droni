import socket
import threading
import time

class Server(threading.Thread): # L'oggetto Server è di tipo thread cosicchè può coesistere simultaneamente al client
    def __init__(self, chatApp): # Inizializza con un riferimento la Chat App e inizializza le variabili
        super(Server, self).__init__()
        self.chatApp = chatApp
        self.port = self.chatApp.port # Recupera la porta del server dai riferimenti della Chat
        self.host = "" # Accetta tutti gli hostnames
        self.hasConnection = False # Stato della connessione
        self.stopSocket = False # Stato di interruzione del socket

        # Comandi di scambio informazioni usati per comunicare tra i peers
        self.commandDict = {
            "nick": [self.setpeerNickname, 1],
            "quit": [self.peerQuit, 0],
            "syntaxErr": [self.chatClientVersionsOutOfSync, 0]
        }

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Crea un nuovo socket
        self.socket.bind((self.host, self.port)) # Lega il socket all'host e alla porta indiicata nelle veraibili del server
        self.socket.listen() # Imposta il socket in ascolto socket

        self.chatApp.sysMsg(self.chatApp.lang['serverStarted'].format(self.port))

    # Metodo per gestire i comandi di scambio informazioni
    def commandHandler(self, command):
        command = command.decode().split(" ")
        if len(command) > 1:
            args = command[1:]
        command = command[0][2:]
        if not command in self.commandDict:
            self.chatApp.sysMsg(self.chatApp.lang['peerInvalidCommand'])
            self.chatApp.chatClient.send("\b/syntaxErr")
        else:
            if self.commandDict[command][1] == 0:
                self.commandDict[command][0]()
            elif len(args) == self.commandDict[command][1]:
                self.commandDict[command][0](args)
            else:
                self.chatApp.sysMsg(self.chatApp.lang['peerInvalidSyntax'])
                self.chatApp.chatClient.send("\b/syntaxErr")

    # Metodo invocato dal threading nella fase iniziale
    def run(self):
        conn, addr = self.socket.accept() # Accetta una connessione
        if self.stopSocket: # Interrompe il socket se l'interrupt è impostato a true
            exit(1)
        init = conn.recv(1024) # Attende le informazioni iniziali dal client
        self.hasConnection = True # Imposta lo stato della connessione  a true
        
        self.handleInit(init)
        
        while True: # loop per la ricezione
            if len(self.chatApp.ChatForm.chatFeed.values) > self.chatApp.ChatForm.y - 10:
                self.chatApp.clearChat()
            data = conn.recv(1024) # Attende i dati
            if not data: # se i dati sono vuoti restituisce un errore
                self.chatApp.sysMsg(self.chatApp.lang['receivedEmptyMessage'])
                self.chatApp.sysMsg(self.chatApp.lang['disconnectSockets'])
                break

            if data.decode().startswith('\b/'): # se i dati sono il comando per lo scambio di informazioni chiama il gestore dei comandi
                self.commandHandler(data)
                if data.decode() == '\b/quit':
                    break
            else: # altrimenti mostra il messaggio nel feed della chat e lo appende nel log della chat
                self.chatApp.messageLog.append("{0} >  {1}".format(self.chatApp.peer, data.decode()))
                self.chatApp.ChatForm.chatFeed.values.append("{0} >  {1}".format(self.chatApp.peer, data.decode()))
                self.chatApp.ChatForm.chatFeed.display()


    def handleInit(self, init):
        if not init: # se l'informazione iniziale è vuota, imposta le variabili del peer come sconosciute
            self.chatApp.peer = "Unknown"
            self.chatApp.peerPort = "unknown"
            self.chatApp.peerIP = 'unknown'
        else: # Decodifica le informazioni iniziali e imposta le variabili del peer ai valori inviati dal peer
            init = init.decode()
            if init.startswith("\b/init"):
                init = init[2:].split(' ')
                self.chatApp.peer = init[1]
                self.chatApp.peerIP = init[2]
                self.chatApp.peerPort = init[3]
            else: # in caso le informazioni iniziali non siano inviate correttamente 
                self.chatApp.peer = "Unknown"
                self.chatApp.peerPort = "unknown"
                self.chatApp.peerIP = 'unknown'

        if not self.chatApp.chatClient.isConnected: # Invia un messaggio per informare circa il connectBack se il socket del client non è connesso
            if self.chatApp.peerIP == "unknown" or self.chatApp.peerPort == "unknown":
                self.chatApp.sysMsg(self.chatApp.lang['failedConnbackPeerUnknown'])
            else:
                self.chatApp.sysMsg(self.chatApp.lang['connbackInfo'])
                self.chatApp.sysMsg(self.chatApp.lang['connbackHostInfo'].format(self.chatApp.peerIP, self.chatApp.peerPort))

        self.chatApp.sysMsg(self.chatApp.lang['peerConnected'].format(self.chatApp.peer)) # Informa l'utente circa il peer

    # Metodo chiamato dalla Chat per resettare il socket del server
    def stop(self):
        if self.hasConnection:
            self.socket.close()
        else:
            self.stopSocket = True
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(('localhost', self.port))
            time.sleep(0.2)
            self.socket.close()
        self.socket = None
        
    # Metodo chiamatp se è stato ricevuto il comando per il cambio del nickname
    def setpeerNickname(self, nick):
        oldNick = self.chatApp.peer
        self.chatApp.peer = nick[0]
        self.chatApp.sysMsg(self.chatApp.lang['peerChangedName'].format(oldNick, nick[0]))

    # Metodo chiamato se peer collegato esce
    def peerQuit(self):
        self.chatApp.sysMsg(self.chatApp.lang['peerDisconnected'].format(self.chatApp.peer))
        self.chatApp.chatClient.isConnected = False
        self.chatApp.restart()

    # Metodo chiamato se il peer collegato usa un comando di scambio informazioni sintatticamente non valido
    def chatClientVersionsOutOfSync(self):
        self.chatApp.sysMsg(self.chatApp.lang['versionOutOfSync'])
        