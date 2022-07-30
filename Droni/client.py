# -*- coding:utf-8 -*-

from pickle import NONE
import socket
import threading
import tkinter as tk

class Client:

    HOST_ADDR = ''
    HOST_PORT = 0
    BUFFER_SIZE = 1024

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    display = None
    ind_entry = None
    drone_entry = None

    def __init__(self, host_addr, host_port):
        self.HOST_PORT = host_port
        self.HOST_ADDR = host_addr
    
    def connect(self, name):
        try:
            self.client.connect((self.HOST_ADDR, self.HOST_PORT))
            self.client.send(name.encode())
            
            threading._start_new_thread(self.receiveMessage, (self.client, "m"))

        except Exception as e:
            print(e)
        
    def sendOrder(self):
        print(self.ind_entry.get() + ':' + self.drone_entry.get())

        bMsg = str.encode(self.ind_entry.get() + ':' + self.drone_entry.get())
        self.client.sendall(bMsg)


    def receiveMessage(self, sck, m):
        while True:
            msgFromServer = self.client.recv(self.BUFFER_SIZE)

            if not msgFromServer: break

            if msgFromServer.startswith("".encode()):
                self.display["text"] = msgFromServer.decode()


        self.client.close()


    def createWindow(self):
        window = tk.Tk()
        window.title("Client")

        # costruiisco il panel per inserire l'indirizzo
        address_frame = tk.Frame(window)
        lbl_addr = tk.Label(address_frame, text = "Indirizzo:")
        lbl_addr.pack(side=tk.LEFT)
        self.ind_entry = tk.Entry(address_frame)
        self.ind_entry.pack(side=tk.LEFT)
        address_frame.pack(side = tk.TOP)

        # costruiisco il panel per inserire il drone di destinazione
        drone_frame = tk.Frame(window)
        lbl_drone = tk.Label(drone_frame, text = "ID/IP Drone:")
        lbl_drone.pack(side=tk.LEFT)
        self.drone_entry = tk.Entry(drone_frame)
        self.drone_entry.pack(side=tk.LEFT)
        drone_frame.pack(side = tk.TOP)
        
        msg_frame = tk.Frame(window)
        self.display = tk.Label(msg_frame, text="").pack()

        # send button
        btn_frame = tk.Frame(window)
        btn_connect = tk.Button(btn_frame, 
                                text="SEND",
                                command=lambda : self.sendOrder())
        btn_connect.pack(side=tk.LEFT)
        btn_frame.pack(side=tk.BOTTOM)


        window.mainloop()

if __name__ == "__main__":
    print('Creating Client...')
    c1 = Client('127.0.0.1', 8080)

    print('Connecting...')
    c1.connect('Client')
    c1.createWindow()