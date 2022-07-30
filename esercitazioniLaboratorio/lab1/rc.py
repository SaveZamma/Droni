#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 20:03:57 2021

@author: apirodd
"""

def contarighe(nomefile):
    conta = 0
    for riga in open(nomefile):
        conta += 1
    return conta
if __name__ == '__main__':
    print(contarighe('rc.py'))