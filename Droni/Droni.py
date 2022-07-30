# -*- coding:utf-8 -*-

import threading
import socket
import tkinter as tk
import time
from gateway import Gateway

class Drone(threading.Thread):

    HOST_ADDR = ''
    HOST_PORT = 0
    BUFFER_SIZE = 1024

    droneId = 0
    droneSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    _isAvailable = True

    def __init__(self, host_addr, host_port, id):
        super().__init__()
        self.HOST_PORT = host_port
        self.HOST_ADDR = host_addr
        self.droneId = id
    
    def __connect(self, name):        
        # self.droneSocket.connect((self.HOST_ADDR, self.HOST_PORT))
        # self.droneSocket.send(name.encode()) # Invia il nome al server dopo la connessione
        #print (f'D{self.droneId}: Connected')
        pass

    @staticmethod
    def __deliver(address):
        print("Drone.deliver" + address)
        
    def __takeOrder(self):
        print("Drone.takeOrder")
        self.__deliver("via aldo moro, 99")

    def sendAvailability(self):
        bMsg = "True" if self._isAvailable else "False"
        print(bMsg)
        #self.droneSocket.sendto(bMsg, (self.HOST_ADDR, self.HOST_PORT))

    def __receiveMessage(self):
        while True:
            msgFromServer, server = self.droneSocket.recvfrom(self.BUFFER_SIZE)

            if not msgFromServer: break

            if msgFromServer.startswith("".encode()):
                self.sendAvailability()



    def __createWindow(self):
        window = tk.Tk()
        window.title("Drone " + self.droneId.__str__())

        # drones side of gateway interface
        drones_frame = tk.Frame(window)
        lblLine = tk.Label(drones_frame, text="Drones Messages")
        lblLine.pack(side=tk.TOP)
        scrollBar = tk.Scrollbar(drones_frame)
        scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        tkDisplay = tk.Text(drones_frame, height=10, width=30)
        tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        scrollBar.config(command=tkDisplay.yview)
        tkDisplay.config(yscrollcommand=scrollBar.set,
                         background="#F4F6F7",
                         highlightbackground="grey",
                         state="disabled")
        drones_frame.pack(side=tk.TOP, pady=(5, 10))

        window.mainloop()

    def run(self):
        self.sendAvailability()
        #self.__receiveMessage()
        self.__createWindow()

if __name__ == "__main__":
    DRONES_NUMBER = 3
    dronesThreads = []

    i = 0
    while i < DRONES_NUMBER:
        print(f'Creating Drone {i+1}...')
        dronesThreads.append(Drone('127.0.0.1', 8080, i+1))

        dronesThreads[i].start()
        #d.join()

        i += 1








