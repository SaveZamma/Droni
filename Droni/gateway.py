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
        print("Ciaoooooo da accept drones")
        while True:
            if len(self.drones) < 2:
                drone, addr = server_d.accept()
                self.drones.append(drone)

                # utilizza un thread in modo da non intasare il thread della gui
                th._start_new_thread(self.send_receive_drones_message, (drone, addr))


    def send_receive_client_message(self, client_connection, client_ip_addr):

        client_name = client_connection.recv(4096)

        #print(client_name)

        while True:
            
            data = client_connection.recv(4096)
            if not data: break

            print("DATA:")
            print(data)

            # TODO Salvo: da sistemare con le lunghezze corrette una volta che si ha un msg di prova
            #order_data = data[0:9]

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


    def __ask_behaviour(self, data):
        available = ""

        res = data.decode().split(":", 1)

        if self.is_drone_ready(res[1]):
            available = "True"
        else:
            available = "False"

        self.client.send(available.encode())



    def send_receive_drones_message(self, drone_connection, drone_ip_addr):
        pass

        # trova l'indice del client, quindi lo rimuove da entrambi gli elenchi (elenco dei nomi dei client e elenco delle connessioni)
        idx = self.get_drone_index(self.drones, drone_connection)
        del self.drones_names[idx]
        del self.drones[idx]
        drone_connection.close()

    # Restituisce l'indice del client corrente nell'elenco dei client
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
