#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 20:08:05 2021

@author: apirodd
"""

fout = open('outpu.txt', 'w')

riga1 = "ip_address = 10.10.10.1, \n"
fout.write(riga1)

riga2 = "mac_address = 00-08-74-4C-7F-1D, \n"
fout.write(riga2)

fout.close()