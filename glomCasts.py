#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 13:20:13 2019

@author: byron
take all available CTD data and post-process thenassemble into gridded master file
"""

import shelve
import os
import numpy
#from matplotlib import dates
from matplotlib import pyplot


def boxcar(series,windowLength):
    l = len(series)
    #l = numpy.shape(series)
    w2 = windowLength//2;
    newSeries = numpy.ones([1,l+windowLength])*numpy.mean(series)
    l2 = numpy.shape(newSeries)
    newSeries[0,(w2+1):(l2[1]-w2)] = series
    output = numpy.zeros([1,l])
    i = 0
    for n in range((w2+1),(l2[1]-w2)):
        output[0,i] = numpy.mean(newSeries[0,(n-w2):(n+w2)])
        if numpy.isnan(output[0,i]):
            print('average not working')
            break
        else:
            i = i+1    
    return output.reshape(numpy.shape(series))

srcDir = '/home/byron/Projects/CTDcasts/castpkl/'
outDir = '/home/byron/Projects/CTDcasts/'
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
station = numpy.zeros([1,l],dtype='int16')
lat = numpy.zeros([1,l],dtype='float32')
lon = numpy.zeros([1,l],dtype='float32')

temp = numpy.zeros([rows,l],dtype='float32')
salt = numpy.zeros([rows,l],dtype='float32')
do = numpy.zeros([rows,l],dtype='float32')
ph = numpy.zeros([rows,l],dtype='float32')
time = numpy.zeros([rows,l],dtype='float64')

i = 0
i2 = 0
#for thing in flist[0:1]:
for thing in flist:
    if thing[5:9] == '0037':        
        continue
    D = shelve.open(srcDir+thing,'r')
    header = D['header']
    cast_data = D['cast_data']
    cast_time = D['cast_time']
    cast_station = D['station']
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
        
    # ***NOTE*** this is ineffeficient and should be done as array
    # Fix it when you know more about what you are doing
    dptht = cast_data[:,headerDict['depth']]
    dot   = cast_data[:,headerDict['diOx']]
    #osatt = cast_data[:,2]
    pht   = cast_data[:,headerDict['ph']]
    tempt = cast_data[:,headerDict['temp']]
    #condt = cast_data[:,5]
    saltt = cast_data[:,headerDict['salt']]
    prest = cast_data[:,headerDict['pres']]
    #flagt = cast_data[:,8]
    [a,b] = numpy.shape(cast_data)
    deltat = 0.25 # header shows sampling rate of 4 Hz
    times = numpy.arange(0,deltat*a,deltat) #relative cast time in seconds
    dt = numpy.diff(times)
    
    ps = boxcar(prest,21)
    ps = ps.reshape(len(prest),)
    dp = numpy.diff(ps)

    dpdt = numpy.divide(dp,dt)
    upi = numpy.where(dpdt < -0.04)
    dni = numpy.where(dpdt > 0.04)
    
    tempu = tempt[upi]
    saltu = saltt[upi]
    dou = dot[upi]
    phu = pht[upi]
    dpthu = dptht[upi]
    timeu = times[upi]
    sm = numpy.argsort(dpthu)
    tempu = tempu[sm]
    saltu = saltu[sm]
    dou = dou[sm]
    phu = phu[sm]
    dpthu = dpthu[sm]
    timeu = timeu[sm]
    del sm
    
    tempd = tempt[dni]
    saltd = saltt[dni]
    dod = dot[dni]
    phd = pht[dni]
    dpthd = dptht[dni]
    timed = times[dni]
    sm = numpy.argsort(dpthd)
    tempd = tempd[sm]
    saltd = saltd[sm]
    dod = dod[sm]
    phd = phd[sm]
    dpthd = dpthd[sm]
    timed = timed[sm]
    
    tempd = boxcar(tempd,3)
    tempu = boxcar(tempu,3)
    saltd = boxcar(saltd,3)
    saltu = boxcar(saltu,3)
    dod = boxcar(dod,3)
    dou = boxcar(dou,3)
    phd = boxcar(phd,3)
    phu = boxcar(phu,3)
    timed = boxcar(timed,3)
    timeu = boxcar(timeu,3)
    
    temp[:,i2] = numpy.interp(uniform_depth,dpthd,tempd,left=numpy.nan,right=numpy.nan)
    temp[:,(i2+1)] = numpy.interp(uniform_depth,dpthu,tempu,left=numpy.nan,right=numpy.nan)

    salt[:,i2] = numpy.interp(uniform_depth,dpthd,saltd,left=numpy.nan,right=numpy.nan)
    salt[:,(i2+1)] = numpy.interp(uniform_depth,dpthu,saltu,left=numpy.nan,right=numpy.nan)
    
    do[:,i2] = numpy.interp(uniform_depth,dpthd,dod,left=numpy.nan,right=numpy.nan)
    do[:,(i2+1)] = numpy.interp(uniform_depth,dpthu,dou,left=numpy.nan,right=numpy.nan)

    ph[:,i2] = numpy.interp(uniform_depth,dpthd,phd,left=numpy.nan,right=numpy.nan)
    ph[:,(i2+1)] = numpy.interp(uniform_depth,dpthu,phu,left=numpy.nan,right=numpy.nan)
    
    time[:,i2] = cast_time+numpy.divide(numpy.interp(uniform_depth,dpthd,timed,left=numpy.nan,right=numpy.nan),86400)
    time[:,(i2+1)] = cast_time+numpy.divide(numpy.interp(uniform_depth,dpthu,timeu,left=numpy.nan,right=numpy.nan),86400)
    #cast.append(thing[5:9]+'down') 
    #cast.append(thing[5:9]+'up') 
    cast[0,i2]= (int(thing[5:9])) 
    cast[0,(i2+1)] = (int(thing[5:9])) 
    lat[0,i2] = position[0]
    lat[0,(i2+1)] = position[0]
    lon[0,i2] = position[1]
    lon[0,(i2+1)] = position[1]
    station[0,i2]= cast_station
    station[0,(i2+1)] = cast_station
    
    # This is a diagnostic plot
    # uncomment to check processing output
    #pyplot.close('all')
#    F1,ax = pyplot.subplots(2,2)
#    ax[0,0].plot(tempt,dptht,linewidth=0.5,color=[0.5,0.5,0.5])
#    ax[0,0].plot(tempt,dptht,'k.',markersize=0.2)
#    ax[0,0].plot(temp[:,i2],uniform_depth,'m.',temp[:,(i2+1)],uniform_depth,'c.')
#    ax[0,0].set_ylim(ax[0,0].get_ylim()[::-1]) #this reverses the yaxis (i.e. deep at the bottom)    
#    
#    ax[1,0].plot(saltt,dptht,linewidth=0.5,color=[0.5,0.5,0.5])
#    ax[1,0].plot(saltt,dptht,'k.',markersize=0.2)
#    ax[1,0].plot(saltt,dptht,'k.',salt[:,i2],uniform_depth,'m.',salt[:,(i2+1)],uniform_depth,'c.')
#    ax[1,0].set_ylim(ax[1,0].get_ylim()[::-1]) #this reverses the yaxis (i.e. deep at the bottom)    
#
#    ax[0,1].plot(dot,dptht,linewidth=0.5,color=[0.5,0.5,0.5])
#    ax[0,1].plot(dot,dptht,'k.',markersize=0.2)
#    ax[0,1].plot(dot,dptht,'k.',do[:,i2],uniform_depth,'m.',do[:,(i2+1)],uniform_depth,'c.')
#    ax[0,1].set_ylim(ax[0,1].get_ylim()[::-1]) #this reverses the yaxis (i.e. deep at the bottom)    
#
#    ax[1,1].plot(pht,dptht,linewidth=0.5,color=[0.5,0.5,0.5])
#    ax[1,1].plot(pht,dptht,'k.',markersize=0.2)
#    ax[1,1].plot(pht,dptht,'k.',ph[:,i2],uniform_depth,'m.',ph[:,(i2+1)],uniform_depth,'c.')
#    ax[1,1].set_ylim(ax[1,1].get_ylim()[::-1]) #this reverses the yaxis (i.e. deep at the bottom)    
#    pyplot.show()
#    pyplot.ion()
    
    
    # clean up workspace for next file
    del [a,b,cast_data,cast_time,deltat,dni,dot,dou,dp,dpdt,dpthd,dptht]
    del [dpthu,dt,header,phd,pht,phu,prest,ps,saltd,saltt,position]
    del [saltu,sm,cast_station,tempd,tempt,tempu,timed,times,timeu,upi,dod]
    
    # do this last in the loop
    i = i+1
    i2 = i2+2
    
    
#    with shelve.open(outDir+outFile,'n') as output:
#        output['position'] = [lat, lon]
#        output['station'] = station
#        output['cast_time'] = cast_time
#        output['header'] = header
#        output['cast_data'] = dataArray
#        
#    output.close()
#    print('Wrote file ' +  outFile + ' to output directory'    
with shelve.open(outDir+'allCasts','n') as output:
    output['cast'] = cast
    output['lon'] = lon
    output['lat'] = lat
    output['station'] = station
    output['time'] = time
    output['temp'] = temp
    output['salt'] = salt
    output['do'] = do
    output['ph'] = ph
    output['depth'] = uniform_depth

output.close()
print('Wrote file ' +  'allCasts' + ' to output directory')