#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The point of this file is to parse the cast_xxxx.dat into useable data.
Maybe save it as a pickle, or ... something else?
22 July 2019
@author: byron

---> Still need to add user input for station # and lat,lon

"""
# Import all packages for use in the script
import os
import numpy
from matplotlib import dates
import shelve
from pathlib import Path
#import sys
import pickle

# declare varaibles for use in the script
srcDir = '/home/byron/Projects/CTDcasts/dat/'
outDir = '/home/byron/Projects/CTDcasts/castpkl/'
devDir = '/home/byron/Projects/CTDcasts/dev/'

flist = os.listdir(srcDir)
flist.sort()
l = len(flist)


dbfile = open(devDir+'castStationDict.pkl', 'rb')      
castStationDict = pickle.load(dbfile) 
#for keys in db: 
#    print(keys, '=>', db[keys]) 
dbfile.close() 
#castStationDict = {}


#for fileName in flist[0:5]:
for fileName in flist:
    m = 0
    outFile = fileName[0:9]+'_shv'
    if Path(outDir+outFile+'.dat').is_file():
        print('output file ->'+ outFile +'<- exists.')
        continue
    else:
        print('creating ->'+ outFile)
        #station = input('Enter the station number associated with ' + fileName +': ')
        #station = int(station)
        castNum=int(fileName[5:9])
        try:
            station = castStationDict[castNum]
        except:
            print('castStationDict keyError using fill value 9')
            station = 9

    file = open(srcDir+fileName)
    isData = 0;
    data = []
    for line in file:
        if isData == 1:
            data.append(line)
        else:
            line = line.strip('\n')
            spLine = line.split(' ')
            if len(spLine)>1 and spLine[1] == 'nquan':
                a = int(spLine[3]) #number of columns / header list size
                header = [' '] * a
                i = 0
            if len(spLine)>1 and spLine[1] == 'name' and i < a:
                ibeg = line.find('=')
                header[i] = line[(ibeg+2):len(line)]
                i = i+1
            if len(spLine)>1 and spLine[1] == 'start_time':
                ibeg = line.find('=')+2
                iend = line.find('[')
                cast_time = dates.datestr2num(line[ibeg:iend])
                
            if spLine[0] == '*END*':
            #if line == '*END*':
                isData = 1
            #if m == 502:
            #    sys.exit('look at this line')
        m = m+1
    file.close()
    
    #outFile = fileName[0:9]+'.pkl'
    m = len(data)
    dataArray = numpy.zeros((m,a)) # m (from len()) rows and a (from file) columns 
    for i in range(0,m):
        k = 0
        line = data[i]
        line = line.strip('\n')
        line = line.split(' ')
        for element in line:
            if element != '':
                dataArray[i,k] = element
                k = k+1
    
    # Associate stations with positions    
    if station == 1:
        lat = 38 + (33.4446/60.0)
        lon = -(76 + (27.8278/60.0))
    elif station == 2:
        lat = 38 + (33.493/60.0)
        lon = -(76 + (26.188/60.0))
    elif station == 3:
        lat = 38 + (38.3022/60.0)
        lon = -(76 + (24.8898/60.0))
    elif station == 4:
        lat = 38 + (32.793/60.0)
        lon = -(76 + (24.162/60.0))
    elif station == 5:
        lat = 38 + (32.2293/60.0)
        lon = -(76 + (23.5942/60.0))
    elif station == 6:
        lat = 38 + (33.365/60.0)
        lon = -(76 + (23.400/60.0))
    else:
        print('in ' + outFile + ' positions are undefined, using fill values')
        lat = 99.9999
        lon = 99.9999        

    with shelve.open(outDir+outFile,'n') as output:
        output['position'] = [lat, lon]
        output['station'] = station
        output['cast_time'] = cast_time
        output['header'] = header
        output['cast_data'] = dataArray
        
    output.close()
    print('Wrote file ' +  outFile + ' to output directory')
    
    # clean up workspace for next file
    del [a,cast_time,data,dataArray,element,header,i,ibeg,iend,isData,k,line]
    del [m,outFile,spLine,station,lat,lon]
       