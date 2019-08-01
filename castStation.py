#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 09:45:55 2019

@author: byron
This script manually creates a new python pickle with a dictionary called
castStatinoDict. This is used in parseCasts to add the station number for 
each cast.
"""

#import os
#import numpy
#from matplotlib import dates
#import shelve
#from pathlib import Path
#import sys
import pickle

# declare varaibles for use in the script
srcDir = '/home/byron/Projects/CTDcasts/dat/'
outDir = '/home/byron/Projects/CTDcasts/dev/'

#flist = os.listdir(srcDir)
#flist.sort()
#l = len(flist)

castStationDict = {}

# 05/15/2019 casts
castStationDict.update({3:1,4:2,5:3,6:4,7:5,8:4,9:3,10:2,11:1,12:2,13:3})
# 05/30/2019 casts
castStationDict.update({14:1,15:2,16:4,17:5})
# 06/20/2019 casts
castStationDict.update({22:1,23:2,24:3,25:4,26:5,27:1,28:2,29:3,30:4,31:5})      
# 07/02/2019 casts
castStationDict.update({32:1,33:2,34:3,35:4,36:5})
# 07/02/2019 casts
castStationDict.update({38:6,39:1,40:2,41:3,42:4,43:5,44:1,45:2,46:3,47:4,48:5,49:6})


# Its important to use binary mode 
dbfile = open(outDir+'castStationDict.pkl', 'ab') 
# source, destination 
pickle.dump(castStationDict, dbfile)                      
dbfile.close()
print('Wrote file ' +  'castStationDict.kl' + ' to output directory')
