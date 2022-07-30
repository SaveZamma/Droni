# -*- coding:utf-8 -*-

from pickle import NONE
import socket
import tkinter as tk

class Client:

    HOST_ADDR = ''
    HOST_PORT = 0

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ind_entry = None
    drone_entry = None

    def __init__(self, host_addr, host_port):
        self.HOST_PORT = host_port
        self.HOST_ADDR = host_addr
    
    def connect(self, name):
        try:
            self.client.connect((self.HOST_ADDR, self.HOST_PORT))
            self.client.send(name.encode())
        except Exception as e:
            print(e)
            #tk.messagebox.showerror(title="ERROR!!!",
            #                        message="Cannot connect to host: " +
            #                        self.HOST_ADDR + " on port: " +
            #                        str(self.HOST_PORT) +
            #                        " Server may be Unavailable. Try again later")
        
    def sendOrder(self):
        print(self.drone_entry.get() + ": " + self.ind_entry.get())

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

        # send button
        btn_frame = tk.Frame(window)
        btn_connect = tk.Button(btn_frame, 
                                text="SEND",
                                command=lambda : self.sendOrder())
        btn_connect.pack(side=tk.LEFT)
        btn_frame.pack(side=tk.BOTTOM)

        window.mainloop()

if __name__ == "__main__":
    c1 = Client('127.0.0.1', 8080)

    c1.connect('Client')
    c1.createWindow()