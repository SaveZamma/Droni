# -*- coding:utf-8 -*-

import threading
import socket
import tkinter as tk
import time
from gateway import Gateway

class Drone(threading.Thread):

    droneId = 0
    HOST_ADDR = ''
    HOST_PORT = 0
    droneSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    available = True

    def __init__(self, host_addr, host_port, id):
        super().__init__()
        self.HOST_PORT = host_port
        self.HOST_ADDR = host_addr
        self.droneId = id
    
    def __connect(self, name):        
        self.droneSocket.connect((self.HOST_ADDR, self.HOST_PORT))
        self.droneSocket.send(name.encode()) # Invia il nome al server dopo la connessione
        print ("Drone.connect")

    @staticmethod
    def __deliver(address):
        print("Drone.deliver" + address)
        
    def __takeOrder(self):
        print("Drone.takeOrder")
        self.__deliver("via aldo moro, 99")

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
        self.__connect('Giacomo')
        self.__takeOrder()
        self.__createWindow()

if __name__ == "__main__":

    i = 0
    while i < 3:

        d = Drone('127.0.0.1', 8080, i)

        d.start()
        #d.join()

        i += 1







