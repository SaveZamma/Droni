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
        window.mainloop()

    def run(self):
        self.__connect('Giacomo')
        self.__takeOrder()
        self.__createWindow()

if __name__ == "__main__":

    d1 = Drone('127.0.0.1', 8080, 1)

    d1.start()
    d1.join()







