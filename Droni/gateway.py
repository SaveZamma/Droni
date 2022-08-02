# -*- coding:utf-8 -*-

from ast import Str
import socket as sk
import tkinter as tk
import threading as th
import queue
from tkinter.tix import WINDOW
    
DRONES_NUMBER = 3
BUFSIZE = 1024

class Gateway:
    WINDOW = None

    server_client = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    server_drones = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    HOST_C_ADDR = '127.0.0.1'
    HOST_C_PORT = 8080
    client = None
    cDisplayer = None

    D_HOST = ('127.168.1.1', 8081)
    DRONES_CONNECTED = [] # Keep track of connected drones as (IP_Address, PORT, ID)
    dSocket = None
    dDisplayer = None
    dMessages = None

    address_to_deliver = ""
    ip_to_deliver = ""
     
    def __init__(self):
        self.createWindow()

        self.server_client.bind((self.HOST_C_ADDR, self.HOST_C_PORT))
        self.server_client.listen(5)  # il server � in ascolto per la connessione del client
        th._start_new_thread(self.accept_client, ())

        self.init_UDP_connection()

        self.WINDOW.mainloop()


    ###########################################################################

    def init_UDP_connection(self):
        self.dSocket = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
        self.dSocket.bind(self.D_HOST)
        self.dMessages = queue.Queue()

        t1 = th.Thread(target=self.UDP_receive)
        t1.start()

    def UDP_receive(self):
        self._printOnDisplayer(self.dDisplayer, f'Listening on {self.D_HOST}')

        self.registerDrones()

        while True:
            try:
                msg, addr = self.dSocket.recvfrom(BUFSIZE)
                self.dMessages.put((msg, addr))
                self._printOnDisplayer(self.dDisplayer, f'{addr} sent: {msg.decode()} ')

                if msg.decode().startswith('AVAILABLE:'):
                    pass

            except:
                print('ERROR: Failed to receive message')

    def registerDrones(self):
        i = 0;
        while i < DRONES_NUMBER:
            msg, sender = self.dSocket.recvfrom(BUFSIZE)

            if msg.decode().startswith('CONNECT_REQUEST:'):
                self.DRONES_CONNECTED.append((sender[0],sender[1], self.calculateDroneID(sender)))

                i = i + 1
        
        self._printOnDisplayer(self.dDisplayer, f'Drones connected: {self.DRONES_CONNECTED}')

    def calculateDroneID(self,sender):
        """Calculates the drone's ID starting from its IP address.
        
            Attributes:
             - `sender`: Tuple (IP, Port)
        """
        return int(sender[0][len(sender[0])-1:])-2

    def is_drone_ready(self,droneID):
        drone = self.getDrone(droneID)
        self.sendToDrone(drone,f'ASK:AVAILABILITY')
        
    def getDrone(self,droneID):
        for drone in self.DRONES_CONNECTED:
            if len(droneID) == 1 and droneID == f'{drone[2]}':
                return drone
            elif droneID == drone[0]:
                return drone
    
    def sendToDrone(self,drone,text):
        try:
            self.dSocket.sendto(text.encode(), (drone[0], drone[1]))
        except:
            print('ERROR: Unable to send message to drone')

    ###########################################################################

    def accept_client(self):
        while True:
            self.client, addr = self.server_client.accept()
            
            # utilizza un thread in modo da non intasare il thread della gui
            th._start_new_thread(self.send_receive_client_message,
                                    (self.client, addr))


    def send_receive_client_message(self, client_connection, client_ip_addr):

        client_name = client_connection.recv(4096)
        self._printOnDisplayer(self.cDisplayer, f'Connecting {client_name.decode()}...')

        while True:
            
            data = client_connection.recv(4096)
            if not data: break
            # print("DATA:")
            # print(data)

            if data.startswith("ASK".encode()):
                self._printOnDisplayer(self.cDisplayer, f'Client asks for drone {data.decode().split(":")[1]} availability')
                self.__ask_behaviour(data)
            elif data.startswith("SEND".encode()):
                self.__send_behaviour(data)

    def __send_behaviour(self, data):
        res = data.decode().split(":", 1)

        msg = {
            "IP_DRONE": res[1],
            "ADDR": res[2]
        }

        print("IP_DRONE: " + msg.get("IP_DRONE") + "\n")
        print("ADDR: " + msg.get("ADDR") + "\n")

        self.ip_to_deliver = msg.get("IP_DRONE")
        self.address_to_deliver = msg.get("ADDR")

        self._sent_drone_message()

    def __ask_behaviour(self, data):
        available = ""

        res = data.decode().split(":", 1)

        if self.is_drone_ready(res[1]):
            available = "True"
        else:
            available = "False"

        self.client.send(available.encode())



   



    def createWindow(self):
        self.WINDOW = tk.Tk()
        self.WINDOW.title("Gateway")

        # client side of gateway interface
        client_frame = tk.Frame(self.WINDOW)
        lblLine = tk.Label(client_frame, text="Client Messages")
        lblLine.pack(side=tk.TOP)
        scrollBar = tk.Scrollbar(client_frame)
        scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        self.cDisplayer = tk.Text(client_frame, height=10, width=30)
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
        self.dDisplayer = tk.Text(drones_frame, height=10, width=30)
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
    

