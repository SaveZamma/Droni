#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 15:30:45 2021

@author: apirodd
"""

import math
def SNR(potenza_segnale, potenza_rumore):
    signal_to_noise_ratio = 10*math.log10(potenza_segnale/potenza_rumore)
    return signal_to_noise_ratio

P_tx = 10 # Watt
P_noise = 9 # Watt

value=SNR(P_tx,P_noise)
print("il valore del SNR è ", value)
