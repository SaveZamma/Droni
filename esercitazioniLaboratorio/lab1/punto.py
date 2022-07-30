#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 19:39:40 2021

@author: apirodd
"""

class Punto:
    """ Rappresenta un punto in un piano."""
    

nuovo = Punto()
nuovo.x = 3.0
nuovo.y = 4.0


#print('(%g,%g)'%(nuovo.x, nuovo.y))

def stampa_punto(p):
    print('(%g,%g)'%(p.x,p.y))

stampa_punto(nuovo)