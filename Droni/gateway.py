# -*- coding:utf-8 -*-

import socket as sk
import tkinter as tk
import threading as th

class Gateway:

    server_client = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    server_drones = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    HOST_C_ADDR = '127.0.0.1'
    HOST_C_PORT = 8080

    HOST_D_ADDR = '127.0.0.2'
    HOST_D_PORT = 8081

    client = None
    drones = []
    drones_names = []
     
    def __init__(self):
        self.server_client.bind((self.HOST_C_ADDR, self.HOST_C_PORT))
        self.server_client.listen(5)  # il server è in ascolto per la connessione del client
        th._start_new_thread(self.accept_client, (self.server_client, " "))

        self.server_drones.bind((self.HOST_D_ADDR, self.HOST_D_PORT))
        self.server_client.listen(5)  # il server è in ascolto per la connessione del client
        # th._start_new_thread(self.accept_drones, (self.server_drones, " "))

    def accept_client(self, server_c, y):
        while True:
            self.client, addr = server_c.accept()

            # utilizza un thread in modo da non intasare il thread della gui
            th._start_new_thread(self.send_receive_client_message,
                                    (self.client, addr))

    def accept_drones(self, server_d, y):
        while True:
            if len(self.drones) < 2:
                drone, addr = server_d.accept()
                self.drones.append(drone)

                # utilizza un thread in modo da non intasare il thread della gui
                th._start_new_thread(self.send_receive_drones_message, (drone, addr))


    def send_receive_client_message(client_connection, client_ip_addr):
        pass

    def send_receive_drones_message(drone_connection, drone_ip_addr):
        pass




    def createWindow(self):
        window = tk.Tk()
        window.title("Gateway")

        # client side of gateway interface
        client_frame = tk.Frame(window)
        lblLine = tk.Label(client_frame, text="Client Messages")
        lblLine.pack(side=tk.TOP)
        scrollBar = tk.Scrollbar(client_frame)
        scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        tkDisplay = tk.Text(client_frame, height=10, width=30)
        tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        scrollBar.config(command=tkDisplay.yview)
        tkDisplay.config(yscrollcommand=scrollBar.set,
                         background="#F4F6F7",
                         highlightbackground="grey",
                         state="disabled")
        client_frame.pack(side=tk.LEFT, pady=(5, 10))

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
        drones_frame.pack(side=tk.RIGHT, pady=(5, 10))

        window.mainloop()


if __name__ == "__main__":
    g = Gateway()
    g.createWindow()
    #c1.connect('Client')
    #c1.createWindow()
