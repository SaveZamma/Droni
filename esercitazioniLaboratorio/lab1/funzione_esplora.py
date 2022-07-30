#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 17:10:11 2021

@author: apirodd
"""

import os

def esplora(dirnome):
    for nome in os.listdir(dirnome):
        percorso = os.path.join(dirnome, nome)
        
        if os.path.isfile(percorso):
            print(percorso)
        else:
            esplora(percorso)
            
esplora('/Users/apirodd/Downloads')