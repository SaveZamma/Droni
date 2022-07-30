#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 14:47:48 2021

@author: apirodd
"""

class Automobile:
    def __init__(self, marca, colore, modello):
        print("Inizializzazione attributi")
        self.marca = marca
        self.colore = colore
        self.modello = modello

prima_macchina = Automobile("Fiat", "Bianca", "500L")
print(prima_macchina.marca)
print(prima_macchina.colore)
print(prima_macchina.modello)
