#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 15:05:09 2019

@author: byron
"""
import numpy
from matplotlib import pyplot

series = numpy.random.randn(1,1024)
windowLength = 7

#def boxcar(series,windowLength):
l = numpy.shape(series)
newSeries = numpy.ones([1,l[1]+windowLength])*numpy.mean(series)
newSeries[0,(w2+1):(l2[1]-w2)] = series
l2 = numpy.shape(newSeries)
w2 = windowLength//2;
output = numpy.zeros([1,l[1]])
i = 0
for n in range((w2+1),(l2[1]-w2)):
    output[0,i] = numpy.mean(newSeries[0,(n-w2):(n+w2)])
    if output[0,i] == 0.0:
        print('average not working')
        break
    else:
        i = i+1
#    return output


x = numpy.arange(0,1024).reshape(1,1024)
pyplot.close(1)
pyplot.figure(1)
pyplot.plot(x[0,:],series[0,:],'r')
pyplot.plot(x[0,:],output[0,:],'b')
pyplot.show()