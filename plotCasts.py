#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 10:01:03 2019

@author: byron
This program loads aligned casts and plots the data. The next step will be to 
unpack all the individual casts and combine them be station and data type.
"""
from matplotlib import pyplot
from matplotlib import dates
import shelve
import os

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
l = len(flist)

for file in flist[30:40]:
#for file in flist:
    D = shelve.open(srcDir+file,'r')
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
        elif item[0] == 'flag:':
            headerDict['flag'] = k
        elif item[0] == '':
            headerDict[''] = k
        k = k+1
#    dpth = cast_data[:,0]
#    diso = cast_data[:,1]
#    osat = cast_data[:,2]
#    pphh = cast_data[:,3]
#    temp = cast_data[:,4]
#    cond = cast_data[:,5]
#    salt = cast_data[:,6]
#    pres = cast_data[:,7]
#    flag = cast_data[:,8]
    dpth = cast_data[:,headerDict['depth']]
    diso   = cast_data[:,headerDict['diOx']]
    #osatt = cast_data[:,2]
    pphh   = cast_data[:,headerDict['ph']]
    temp = cast_data[:,headerDict['temp']]
    #condt = cast_data[:,5]
    salt = cast_data[:,headerDict['salt']]
    pres = cast_data[:,headerDict['pres']]

    
    # example code
    #fig, axs = plt.subplots(1, 3, figsize=(9, 3), sharey=True)
    fig,ax = pyplot.subplots(1,5,sharey=True)
    fig.suptitle(file[0:9]+ ' station: ' + str(station) + ' ' + str(dates.num2date(cast_time)))
    ax[0].plot(temp,dpth,linewidth='0.5',color='b',marker='.',markersize=2,markeredgecolor='r',markerfacecolor='r',label='temp')
    ax[0].set_ylabel('Depth [m]')
    ax[0].set_ylim(ax[0].get_ylim()[::-1]) #this reverses the yaxis (i.e. deep at the bottom)
    ax[0].set_xlabel('Temperature [C]')
    ax[0].xaxis.set_label_position('top') # this moves the label to the top
    ax[0].xaxis.set_ticks_position('top') # this moves the ticks to the top

    ax[1].plot(diso,dpth,linewidth='0.5',color='b',marker='.',markersize=2,markeredgecolor='r',markerfacecolor='r',label='do')
    ax[1].set_xlabel('O_2 [mg/l]')
    ax[1].xaxis.set_label_position('bottom') # this moves the label to the top
    ax[1].xaxis.set_ticks_position('bottom') # this moves the ticks to the top
    
    ax[2].plot(salt,dpth,linewidth='0.5',color='b',marker='.',markersize=2,markeredgecolor='r',markerfacecolor='r',label='salt')
    ax[2].set_xlabel('salinity [PSU]')
    ax[2].xaxis.set_label_position('top') # this moves the label to the top
    ax[2].xaxis.set_ticks_position('top') # this moves the ticks to the top

#    ax[3].plot(osat,dpth,linewidth='0.5',color='b',marker='.',markersize=2,markeredgecolor='r',markerfacecolor='r',label='dosat')
#    ax[3].set_xlabel('O_2 [%]')
#    ax[3].xaxis.set_label_position('bottom') # this moves the label to the top
#    ax[3].xaxis.set_ticks_position('bottom') # this moves the ticks to the top

    ax[4].plot(pphh,dpth,linewidth='0.5',color='b',marker='.',markersize=2,markeredgecolor='r',markerfacecolor='r',label='ph')
    ax[4].set_xlabel('log_10(H)')
    ax[4].xaxis.set_label_position('top') # this moves the label to the top
    ax[4].xaxis.set_ticks_position('top') # this moves the ticks to the top
    