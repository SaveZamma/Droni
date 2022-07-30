#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 16:28:40 2021

@author: apirodd
"""

import os
print('il percorso assoluto del file words.txt è:',os.path.abspath('words.txt'))
print('')
print('oggetto words.txt è una directory?', os.path.isdir('words.txt'))
print('')
print('oggetto /Users/apirodd è una directory?', os.path.isdir('/Users/apirodd'))
