#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 15:14:13 2021

@author: apirodd
"""

class Gag:
    def __init__(self, titolo):
        self.titolo = titolo
    def __str__(self):
        return "Sono la gag '{}0)'".format(self.titolo)

spam = Gag("Spam, spam, spam")
print(str(spam))