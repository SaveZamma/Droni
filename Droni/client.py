# -*- coding:utf-8 -*-

from pickle import NONE
import socket
import threading
import tkinter as tk
import time

class Client:

    HOST_ADDR = ''
    HOST_PORT = 0
    BUFFER_SIZE = 1024

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    display = None

    drone_var = None
    ind_entry = None
    drone_entry = None

    btn_connect = None
    btn_ask = None

    available = "False"

    def __init__(self, host_addr, host_port):
        self.HOST_PORT = host_port
        self.HOST_ADDR = host_addr
    
    def connect(self, name):
        try:
            self.client.connect((self.HOST_ADDR, self.HOST_PORT))

            msg = str(time.time()) + '|' + name
            self.client.send(msg.encode())
            
            threading._start_new_thread(self.receiveMessage, ())
            print(f'Successfully connected to {self.HOST_ADDR}')
        except Exception as e:
            print(e)
        
    def sendOrder(self):
        print(self.drone_entry.get() + ':' + self.ind_entry.get())

        bMsg = str.encode(str(time.time()) + '|' + "SEND:" + self.drone_entry.get() + ':' + self.ind_entry.get())
        self.client.sendall(bMsg)

        # riazzero il msg di disponibilità

        self.available = "False"
        self.enable_send_btn()

    def ask_availability(self, *args):
        self.available = 'False'
        self.enable_send_btn()

        if len([*self.drone_entry.get()]) == 1 or len(self.drone_entry.get().split('.')) >= 4:
            
            bMsg = str.encode(str(time.time()) + '|' + "ASK:" + self.drone_entry.get())
            self.client.sendall(bMsg)
        else :
            self._printOnDisplay('Invalid name format')

    def receiveMessage(self):
        while True:
            msgFromServer = self.client.recv(self.BUFFER_SIZE)

            if not msgFromServer: break

            msg_t = msgFromServer.decode()

            msg = msg_t.split("|")

            TCP_time = msg[0]
            TCP_delivery_time = time.time() - float(TCP_time)
            self._printOnDisplay(f'TCP package delivery time: {TCP_delivery_time} ')

            msg_client = msg[1].split(':')

            if msg_client[0] == 'ASK':
                self.showAvailability(msg_client)

        self.client.close()

    def showAvailability(self,serverMsg):
        self.available = serverMsg[2]
        if self.available == 'True':
            self.enable_send_btn()

        text = f'Drone {serverMsg[1]} is '
        text += 'available' if serverMsg[2] == 'True' else 'not available'

        self._printOnDisplay(text)

    def enable_send_btn(self):
        if self.available == "True":
            self.btn_connect.config(state=tk.NORMAL)
        else:
            self.btn_connect.config(state=tk.DISABLED)


    def createWindow(self):
        window = tk.Tk()
        window.title("Client")

        self.drone_var = tk.StringVar()

        # costruiisco il panel per inserire il drone di destinazione
        drone_frame = tk.Frame(window)
        lbl_drone = tk.Label(drone_frame, text = "ID/IP Drone:")
        lbl_drone.pack(side=tk.LEFT)
        self.drone_entry = tk.Entry(drone_frame, textvariable=self.drone_var)
        self.drone_var.trace("w", self.ask_availability)
        self.drone_entry.pack(side=tk.LEFT)
        drone_frame.pack(side = tk.TOP)

        # costruiisco il panel per inserire l'indirizzo
        address_frame = tk.Frame(window)
        lbl_addr = tk.Label(address_frame, text = "Indirizzo:")
        lbl_addr.pack(side=tk.LEFT)
        self.ind_entry = tk.Entry(address_frame)
        self.ind_entry.pack(side=tk.LEFT)
        address_frame.pack(side = tk.TOP)
        
        msg_frame = tk.Frame(window)
        self.display = tk.Label(msg_frame, text="")
        self.display.pack(side=tk.TOP)
        msg_frame.pack(side = tk.BOTTOM)

        # send button
        btn_frame = tk.Frame(window)
        self.btn_connect = tk.Button(btn_frame, 
                                text="SEND",
                                command=lambda : self.sendOrder())
        self.btn_connect.pack(side=tk.LEFT)
        btn_frame.pack(side=tk.BOTTOM)

        # client display
        client_frame = tk.Frame(window)
        scrollBar = tk.Scrollbar(client_frame)
        scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

        self.display = tk.Text(client_frame, height=15, width=40)
        self.display.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))

        scrollBar.config(command=self.display.yview)
        self.display.config(yscrollcommand=scrollBar.set,
                         background="#F4F6F7",
                         highlightbackground="grey",
                         state="disabled")

        client_frame.pack(side=tk.TOP, pady=(5, 10))
        self.display.insert(tk.END, 'Client START')

        self.enable_send_btn()

        window.mainloop()

    def _printOnDisplay(self,text):
        print(text)
        self.display.config(state=tk.NORMAL)
        self.display.insert(tk.END, text+"\n")
        self.display.config(state=tk.DISABLED)

if __name__ == "__main__":
    print('Creating Client...')
    c1 = Client('127.0.0.1', 8080)

    print('Connecting...')
    c1.connect('Client')
    c1.createWindow()