# -*- coding:utf-8 -*-

import socket as sk
import threading
import random as rnd
import tkinter as tk
from token import NEWLINE
import time

DRONES_NUMBER = 3
dronesThreads = []

HOST = ('127.168.1.1', 8081)
BUFSIZE = 1024

class Drone(threading.Thread):
    ID = 0
    IP_ADDR = ''
    isAvailable = True
    droneSocket = None

    display = None

    def __init__(self, dorneAddress, id):
        super().__init__()
        self.ID = id
        self.IP_ADDR = dorneAddress

        # Define Host's IP and Port
        self.droneSocket = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

        # Bind to client's IP and Port. 
        # Different clients should have different ports, that's why we use randint() here
        self.droneSocket.bind((dorneAddress, rnd.randint(8000,9000)))
        

    def sendAvailability(self):
        msg = "True" if self.isAvailable else "False"
        msg = 'AVAILABLE:' + msg
        try:
            self.droneSocket.sendto(msg.encode(), (HOST[0], HOST[1]))
            print(f'Drone {self.ID}: {msg}')
        except:
            print('ERROR: Could not send message to server')


    def receive(self):
        while True:
            try:
                msg, _ = self.droneSocket.recvfrom(BUFSIZE)
                print(f'{self.ID} Received: {msg.decode()}'+ NEWLINE)


            except:
                print('ERROR: Could not receive message from server')


    def run(self):
        t = threading.Thread(target=self.receive)
        t.start()

        self.sendAvailability()
        self.__createWindow()


    def __createWindow(self):
        window = tk.Tk()
        window.title("Drone " + self.ID.__str__())

        # drones side of gateway interface
        drones_frame = tk.Frame(window)
        lblLine = tk.Label(drones_frame, text="Drones Messages")
        lblLine.pack(side=tk.TOP)

        scrollBar = tk.Scrollbar(drones_frame)
        scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

        self.display = tk.Text(drones_frame, height=10, width=30)
        self.display.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))

        scrollBar.config(command=self.display.yview)
        self.display.config(yscrollcommand=scrollBar.set,
                         background="#F4F6F7",
                         highlightbackground="grey",
                         state="disabled")

        drones_frame.pack(side=tk.TOP, pady=(5, 10))
        self.display.insert(tk.END, 'Drone START')

        window.mainloop()

    



if __name__ == '__main__':
    baseIP = '127.168.1.'

    i = 0
    while i < DRONES_NUMBER:
        d = Drone(f'{baseIP}{i+2}',i)
        dronesThreads.append(d)
        print(f'Starting Drone {i}...')
        d.start()

        i = i+1








