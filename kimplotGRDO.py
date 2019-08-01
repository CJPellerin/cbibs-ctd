#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 11:44:46 2019

@author: byron
"""

import shelve
import os
import numpy
from matplotlib import dates
from matplotlib import pyplot
from matplotlib import axes

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

srcDir = '/home/byron/Projects/CTDcasts/'
outDir = '/home/byron/Projects/CTDcasts/'

D = shelve.open(srcDir+'allCasts','r')
time = D['time']
station = D['station']
salt = D['salt']
temp = D['temp']
do = D['do']
depth = D['depth']
cast = D['cast']
lat = D['lat']
lon = D['lon']
D.close()

[a,ind] = numpy.where(station==5)
tempt = temp[4:,ind]
saltt = salt[4:,ind]
dot = do[4:,ind]
cast_time = time[4:,ind]
dpth = depth[4:]    
# %%
strTimes = []
cast_times = dates.num2date(time[1,ind])
for n in [0,6,8,10]:
    strTimes.append(cast_times[n].strftime('%m/%d/%Y'))

# %%

pyplot.close(1)
#F1 = pyplot.figure(1)
#A1 = F1.add_axes([0.1,0.1,0.8,0.8])
F1,[A1,A2,A3] = pyplot.subplots(1,3,sharey=True)

A1.plot(dot[:,0],dpth,linewidth='0.5',color='b',marker='o',markersize=1.5,markeredgecolor='b',markerfacecolor='b',label=strTimes[0])
A1.plot(dot[:,6],dpth,linewidth='0.5',color='r',marker='o',markersize=1.5,markeredgecolor='r',markerfacecolor='r',label=strTimes[1])
A1.plot(dot[:,8],dpth,linewidth='0.5',color='g',marker='o',markersize=1.5,markeredgecolor='g',markerfacecolor='g',label=strTimes[2])
A1.plot([2,2],[0,25],'--',color=[0.2,0.2,0.2])
A1.plot([5,5],[0,25],'--',color=[0.2,0.2,0.2])
# set A1 axes properties
A1.grid(True,linestyle='--')
A1.set_position([0.1,0.1,0.2666,0.8])
A1.set_xticks([0,2,5,10])
A1.set_xlim([0,11])
A1.set_ylim([25,0])
A1.set_xlim([0,10])
A1.set_ylabel('Depth [m]')
A1.set_ylim([25,0])
A1.set_xlabel('[mg/l]')
A1.set_xlim([0,12])
A1.set_xticks([0,2,5,10])
A1.set_title('Dissolved Oxygen')

A1.legend()
#A1.show()

#A2 = F1.add_axes([0.1,0.1,0.8,0.8])
A2.set_position([0.3666,0.1,0.2666,0.8])
A2.plot(saltt[:,0],dpth,linewidth='0.5',color='b',marker='o',markersize=1.5,markeredgecolor='b',markerfacecolor='b',label=strTimes[0])
A2.plot(saltt[:,6],dpth,linewidth='0.5',color='r',marker='o',markersize=1.5,markeredgecolor='r',markerfacecolor='r',label=strTimes[1])
A2.plot(saltt[:,8],dpth,linewidth='0.5',color='g',marker='o',markersize=1.5,markeredgecolor='g',markerfacecolor='g',label=strTimes[2])
# set A2 axes properties
A2.set_xlabel('[PSU]')
A2.set_xlim([5,20])
A2.set_xticks([10,15])
A2.set_title('Salinity')
A2.grid(True,linestyle='--')


A3.plot(tempt[:,0],dpth,linewidth='0.5',color='b',marker='o',markersize=1.5,markeredgecolor='b',markerfacecolor='b',label=strTimes[0])
A3.plot(tempt[:,6],dpth,linewidth='0.5',color='r',marker='o',markersize=1.5,markeredgecolor='r',markerfacecolor='r',label=strTimes[1])
A3.plot(tempt[:,8],dpth,linewidth='0.5',color='g',marker='o',markersize=1.5,markeredgecolor='g',markerfacecolor='g',label=strTimes[2])
# set A3 axes properties
A3.set_title('Temperature')
A3.set_position([0.6333,0.1,0.2666,0.8])
A3.set_ylim([25,0])
A3.set_xlabel('[C]')
A3.set_xlim([15,30])
A3.set_xticks([20,25,30])
A3.grid(True,linestyle='--')
F1.suptitle('Vertical profiles in the Choptank River channel')
pyplot.show()
