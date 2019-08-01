#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 14:50:22 2019

@author: byron
"""

import shelve
import os
import numpy
#from matplotlib import dates
from matplotlib import pyplot

srcDir = '/home/byron/Projects/CTDcasts/castpkl/'
dirList = os.listdir(srcDir)
# get list of all .dat files in the directory
flist = []
for names in dirList:
    if names.endswith(".dat"):
        a = names.find('.')
        flist.append(names[0:a])
#print(flist[0])
flist.sort()
l = len(flist)*2
uniform_depth = numpy.arange(0,30,0.25)
rows = len(uniform_depth)

cast = numpy.zeros([1,l],dtype='int16')
lat = numpy.zeros([1,l],dtype='float32')
lon = numpy.zeros([1,l],dtype='float32')

temp = numpy.zeros([rows,l],dtype='float32')
salt = numpy.zeros([rows,l],dtype='float32')
do = numpy.zeros([rows,l],dtype='float32')
ph = numpy.zeros([rows,l],dtype='float32')
time = numpy.zeros([rows,l],dtype='float64')

i = 0
i2 = 0
for thing in flist[10:11]:
#for thing in flist:
    if thing[5:9] == '0037':        
        continue
    D = shelve.open(srcDir+thing,'r')
    header = D['header']
    cast_data = D['cast_data']
    cast_time = D['cast_time']
    station = D['station']
    position = D['position']
    D.close()
    
    k = 0
    headerDict = {}
    for item in header:
        item = item.split(' ')
        if item[0] == 'depSM:':
            headerDict['depth'] = k
        elif item[0] == 'sbeox0Mg/L:':
            headerDict['diOx'] = k
        elif item[0] == 'ph:':
            headerDict['ph'] = k
        elif item[0] == 'tv290C:':
            headerDict['temp'] = k
        elif item[0] == 'sal00:':
            headerDict['salt'] = k
        elif item[0] == 'prdM:':
            headerDict['pres'] = k
        k = k+1
    