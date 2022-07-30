#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 16:11:37 2021

@author: apirodd
"""

class Tempo:
    """Rappresenta un'ora del giorno
    attributi: ora, minuto, secondo
    """
tempo = Tempo()
tempo.ora = 11
tempo.minuto = 59
tempo.secondo = 30
#all'interno della classe Tempo
def __init__(self, ora=0, minuto=0, secondo=0): 
    self.ora = ora
    self.minuto = minuto
    self.secondo = secondo
        
def __str__(self):
    return '%.2d:%.2d:%2d'%(self.ora, self.minuto, self.secondo)

