# -*- coding:utf-8 -*-

from ast import Str
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

    address_to_deliver = ""
    ip_to_deliver = ""
     
    def __init__(self):
        self.server_client.bind((self.HOST_C_ADDR, self.HOST_C_PORT))
        self.server_client.listen(5)  # il server è in ascolto per la connessione del client
        th._start_new_thread(self.accept_client, ())

        self.server_drones.bind((self.HOST_D_ADDR, self.HOST_D_PORT))
        th._start_new_thread(self.accept_drones, ())

    def accept_client(self):
        while True:
            self.client, addr = self.server_client.accept()
            
            # utilizza un thread in modo da non intasare il thread della gui
            th._start_new_thread(self.send_receive_client_message,
                                    (self.client, addr))

    def accept_drones(self):
        while True:
            data, address = self.server_drones.recvfrom(4096)

            self.drones.append(data)

            th._start_new_thread(self._receive_drones_message, (data, address))


    def send_receive_client_message(self, client_connection, client_ip_addr):

        client_name = client_connection.recv(4096)

        while True:
            
            data = client_connection.recv(4096)
            if not data: break

            print("DATA:")
            print(data)

            if data.startswith("ASK".encode()):
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


    def _receive_drones_message(self, drone_connection, drone_ip_addr):     
        
        drone_name = drone_connection.recv(4096)

        while True:

            data = drone_connection.recvfrom(4096)
            if not data: break

            print("DATA:")
            print(data)

            res = data.decode().split(":", 1)

            self.drones_names.append(res[1])

    def _sent_drone_message(self):
        self.server_drones.sendto(self.address_to_deliver.encode(), self.ip_to_deliver)


    # Restituisce l'indice del drone corrente nell'elenco dei droni
    def get_drone_index(self, curr_drone):
        idx = 0
        for conn in self.drones:
            if conn == curr_drone:
                break
            idx = idx + 1

        return idx

    # Indica se il drone è diponibile
    def is_drone_ready(self, drone_ip):
        for d in self.drones:
            if d == drone_ip:
                return True
        return False



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
