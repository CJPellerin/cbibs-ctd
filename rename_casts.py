#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 10:31:57 2019

@author: byron
"""

import os
#          /home/byron/Projects/CTDcasts/dat/
srcDir = '/home/byron/Projects/CTDcasts/dat/'

flist = os.listdir(srcDir)
a = len(flist) # get the length of the list for the loop 
for name in flist:
    tsrt = name
    words = name.split('_')
    num = words[5]
    if len(num) == 2:
        num = '00' + num
    if len(num) == 3:
        num = '0' + num
    if len(num) > 4:
        num = 'XXXX'

    outname = 'cast_' + num +'.dat'
    print(outname)
    os.rename(srcDir+name, srcDir+outname)     

