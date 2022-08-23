# -*- coding:utf-8 -*-

from ast import Str
import socket as sk
import tkinter as tk
import threading as th
import queue
import time
    
DRONES_NUMBER = 3
BUFSIZE = 1024

class Gateway:
    WINDOW = None

    server_client = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    server_drones = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    CLIENT_IP = '10.10.10.1'
    CLIENT_PORT = 8080
    client = None
    cDisplayer = None

    DRONES_NETWORK = ('192.168.1.1', 8081)
    DRONES_CONNECTED = [] # Keep track of connected drones as (IP_Address, PORT, ID)
    dSocket = None
    dDisplayer = None
    dMessages = None


    def __init__(self):
        self.createWindow()

        self.server_client.bind(('localhost', self.CLIENT_PORT))
        self.server_client.listen(5)  # il server � in ascolto per la connessione del client
        #th._start_new_thread(self.accept_client, ())
        t = th.Thread(target=self.accept_client)
        t.start()

        self.init_UDP_connection()

        self.WINDOW.mainloop()


    ###########################################################################

    def init_UDP_connection(self):
        self.dSocket = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
        self.dSocket.bind(('localhost', 8081))
        self.dMessages = queue.Queue()

        t1 = th.Thread(target=self.UDP_receive)
        t1.start()

    def UDP_receive(self):
        self._printOnDisplayer(self.dDisplayer, f'Listening on {self.DRONES_NETWORK}')

        self.registerDrones()

        while True:
            try:
                msg_t, addr = self.dSocket.recvfrom(BUFSIZE)
                msg_t = msg_t.decode()
                drone = self._findDrone(addr)
                self.dMessages.put((msg_t, addr))
                self._printOnDisplayer(self.dDisplayer, f'{drone[0:2]} sent: {msg_t} ')

                msg = msg_t.split("|")

                UDP_time = msg[0]
                UDP_delivery_time = time.time() - float(UDP_time)
                self._printOnDisplayer(self.dDisplayer, f'UDP package delivery time: {UDP_delivery_time} ')

                sent_msg = msg[1]
                self.dMessages.put((sent_msg, addr))
                self._printOnDisplayer(self.dDisplayer, f'{addr} sent: {sent_msg} ')

                if sent_msg.startswith('AVAILABLE:'):
                    data = sent_msg.split(':')
                    self._answerAvailability(data[1], data[2])
                
                if sent_msg.startswith('DELIVERY:'):
                    pass
                
            except:
                print('ERROR: Failed to receive message')

    def registerDrones(self):
        i = 0;
        while i < DRONES_NUMBER:
            msg_t, sender = self.dSocket.recvfrom(BUFSIZE)

            msg_t = msg_t.decode()

            msg = msg_t.split("|")

            UDP_time = msg[0]
            UDP_delivery_time = time.time() - float(UDP_time)
            self._printOnDisplayer(self.dDisplayer, f'UDP package delivery time: {UDP_delivery_time} ')

            if msg[1].startswith('CONNECT_REQUEST:'):
                droneID = i;
                drone_ip = f'192.168.1.{droneID+1}'
                self.DRONES_CONNECTED.append((drone_ip, sender[1], droneID))

            i = i + 1
        
        self._printOnDisplayer(self.dDisplayer, f'Drones connected: {self.DRONES_CONNECTED}')

    def _findDrone(self,sender):
        for drone in self.DRONES_CONNECTED:
            if (drone[1] == sender[1]):
                return drone


    def is_drone_ready(self,droneID):
        drone = self._getDrone(droneID)
        if drone is None:
            self._answerAvailability(droneID, False)
            return False
        self._sendToDrone(drone, (str(time.time()) + '|' + f'ASK:AVAILABILITY'))
        
    def _getDrone(self,droneID):
        for drone in self.DRONES_CONNECTED:
            if len(droneID) == 1 and droneID == f'{drone[2]}':
                return drone
            elif droneID == drone[0]:
                return drone
    
    def _sendToDrone(self,drone,text):
        try:
            self.dSocket.sendto(text.encode(), ('localhost', drone[1]))
        except:
            print('ERROR: Unable to send message to drone')

    def _sendDelivery(self,droneID,address):
        drone = self._getDrone(droneID)
        if drone is not None:
            msg = f'DELIVERY:{address}'
            self._sendToDrone(drone, (str(time.time()) + '|' + msg))


    ###########################################################################

    def accept_client(self):
        while True:
            self.client, addr = self.server_client.accept()
            
            # utilizza un thread in modo da non intasare il thread della gui
            th._start_new_thread(self.send_receive_client_message,
                                    (self.client, addr))


    def send_receive_client_message(self, client_connection, client_ip_addr):

        msgFromClient = client_connection.recv(4096)

        msg_t = msgFromClient.decode()

        msg = msg_t.split("|")

        TCP_time = msg[0]
        TCP_delivery_time = time.time() - float(TCP_time)
        self._printOnDisplayer(self.cDisplayer, f'TCP package delivery time: {TCP_delivery_time} ')

        client_name = msg[1]

        self._printOnDisplayer(self.cDisplayer, f'{client_name} connected on {self.CLIENT_IP}')

        while True:
            
            msgFromClient = client_connection.recv(4096)
            if not msgFromClient: break

            msg_t = msgFromClient.decode()

            msg = msg_t.split("|")

            TCP_time = msg[0]
            TCP_delivery_time = time.time() - float(TCP_time)
            self._printOnDisplayer(self.cDisplayer, f'TCP package delivery time: {TCP_delivery_time} ')

            data = msg[1]

            if data.startswith("ASK"):
                self._printOnDisplayer(self.cDisplayer, f'Client asks for drone {data.split(":")[1]} availability')
                self.__ask_behaviour(data)
                
            elif data.startswith("SEND"):
                self._printOnDisplayer(self.cDisplayer, f'Delivery order for drone {data.split(":")[1]}')
                self.__send_behaviour(data)

    def __send_behaviour(self, data):
        res = data.split(":")

        droneID = res[1]
        deliveryAddress = res[2]

        print("ID_DRONE: " + droneID + "\n")
        print("ADDR: " + deliveryAddress + "\n")
        self._printOnDisplayer(self.cDisplayer, f'{droneID} -> {deliveryAddress}')

        self._sendDelivery(droneID, deliveryAddress)

    def __ask_behaviour(self, data):
        # available = ""

        res = data.split(":", 1)
        self.is_drone_ready(res[1])

    def _answerAvailability(self, droneID, isAvailable):
        msg = str(time.time()) + '|'
        msg += 'ASK:'
        msg += f'{droneID}:'
        msg += 'True' if isAvailable else 'False'
        self.client.send(msg.encode())

   

    def createWindow(self):
        self.WINDOW = tk.Tk()
        self.WINDOW.title("Gateway")

        # client side of gateway interface
        client_frame = tk.Frame(self.WINDOW)
        lblLine = tk.Label(client_frame, text="Client Messages")
        lblLine.pack(side=tk.TOP)
        scrollBar = tk.Scrollbar(client_frame)
        scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        self.cDisplayer = tk.Text(client_frame, height=20, width=50)
        self.cDisplayer.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        scrollBar.config(command=self.cDisplayer.yview)
        self.cDisplayer.config(yscrollcommand=scrollBar.set,
                         background="#F4F6F7",
                         highlightbackground="grey",
                         state="disabled")
        client_frame.pack(side=tk.LEFT, pady=(5, 10))

        # drones side of gateway interface
        drones_frame = tk.Frame(self.WINDOW)
        lblLine = tk.Label(drones_frame, text="Drones Messages")
        lblLine.pack(side=tk.TOP)
        scrollBar = tk.Scrollbar(drones_frame)
        scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        self.dDisplayer = tk.Text(drones_frame, height=20, width=50)
        self.dDisplayer.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        scrollBar.config(command=self.dDisplayer.yview)
        self.dDisplayer.config(yscrollcommand=scrollBar.set,
                         background="#F4F6F7",
                         highlightbackground="grey")
        drones_frame.pack(side=tk.RIGHT, pady=(5, 10))


    def _printOnDisplayer(self,display,text):
        print(text)
        display.config(state=tk.NORMAL)
        display.insert(tk.END, text+"\n")
        display.config(state=tk.DISABLED)


if __name__ == "__main__":
    g = Gateway()  
