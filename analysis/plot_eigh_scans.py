#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 19:36:15 2019

@author: stephey
"""
import numpy as np
from matplotlib import pyplot as plt
import pickle


#what do you want to load
#loaddata = 'skylake'
#loaddata = 'volta'
loaddata = 'haswell'
#loaddata = 'knl'
loadstring = '/Users/stephey/Dropbox/NERSC/Work/Dates/20190522/eigh_' + str(loaddata) + '.pickle'

#should load mdiv_data
with open(loadstring, 'rb') as handle:
    nresults = pickle.load(handle)
    
    
#also plot theoretical values
#eigh should go as order N3
#little matrix should go as m times 
#There's a theoretical prediction right?  
#You could plot that, scaled relative to the slowest (mdiv1) for each setup
    
#plot eigh scans
msizes = [100, 500, 1000, 5000, 10000, 15000]
mdivs = [1,2,5,10]
    
mtheory = np.zeros((len(msizes),len(mdivs)))
#loop over msizes
for i in range(len(msizes)):
    msize = int(msizes[i])
    #loop over mdivs
    for j in range(len(mdivs)):
        mdiv = int(mdivs[j])
        #generate theoretical value to show on plot
        mtheory[i,j] = (msize**3) / (mdiv**2)

# set width of bar
barWidth = 0.25

#throw away the first trial
#these contain all 5 trials for all n matrices
mdiv1_all = nresults[:,:,0]
mdiv2_all = nresults[:,:,1]
mdiv5_all = nresults[:,:,2]
mdiv10_all = nresults[:,:,3]

#get mean and std but throw away first trial
mdiv1 = np.mean(mdiv1_all[1:,:],axis=0)
mdiv2 = np.mean(mdiv2_all[1:,:],axis=0)
mdiv5 = np.mean(mdiv5_all[1:,:],axis=0)
mdiv10 = np.mean(mdiv10_all[1:,:],axis=0)

mdiv1_std = np.std(mdiv1_all[1:,:],axis=0)
mdiv2_std = np.std(mdiv2_all[1:,:],axis=0)
mdiv5_std = np.std(mdiv5_all[1:,:],axis=0)
mdiv10_std = np.std(mdiv10_all[1:,:],axis=0)

#scale theoretical values to mdiv1
mtheory_scaled = np.zeros_like(mtheory)
for i in range(len(msizes)):
    mtheory_scaled[i,:] = mtheory[i,:] * mdiv1[i]

mtheory100 = mtheory_scaled[0,:] / mtheory[0,0]
mtheory500 = mtheory_scaled[1,:] / mtheory[1,0]
mtheory1000 = mtheory_scaled[2,:] / mtheory[2,0]
mtheory5000 = mtheory_scaled[3,:] / mtheory[3,0]
mtheory10000 = mtheory_scaled[4,:] / mtheory[4,0]
mtheory15000 = mtheory_scaled[5,:] / mtheory[5,0]

# Set position of bar on X axis
r1 = np.arange(len(mdiv1))
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]
r4 = [x + barWidth for x in r3]

# and make axes for theory lines
#this is stupid but it works
t1 = [r1[0],r2[0],r3[0],r4[0]] 
t2 = [r1[1],r2[1],r3[1],r4[1]]
t3 = [r1[2],r2[2],r3[2],r4[2]]
t4 = [r1[3],r2[3],r3[3],r4[3]] 
t5 = [r1[4],r2[4],r3[4],r4[4]]
t6 = [r1[5],r2[5],r3[5],r4[5]]  
 
# Make the plot
plt.figure()
plt.bar(r1, mdiv1, color='#7f6d5f', width=barWidth, yerr=mdiv1_std, edgecolor='white', label='m=1')
plt.bar(r2, mdiv2, color='#557f2d', width=barWidth, yerr=mdiv2_std, edgecolor='white', label='m=2')
plt.bar(r3, mdiv5, color='#2d7f5e', width=barWidth, yerr=mdiv5_std, edgecolor='white', label='m=5')
plt.bar(r4, mdiv10, color='cyan', width=barWidth, yerr=mdiv10_std, edgecolor='white', label='m=10')
plt.plot(t1, mtheory100, color='black', label='theory')
plt.plot(t2, mtheory500, color='black')
plt.plot(t3, mtheory1000, color='black')
plt.plot(t4, mtheory5000, color='black')
plt.plot(t5, mtheory10000, color='black')
plt.plot(t6, mtheory15000, color='black')
 
# Add xticks on the middle of the group bars
plt.xlabel('Matrix Size', fontweight='bold')
plt.xticks([r + barWidth for r in range(len(mdiv1))], msizes)
plt.ylim((1E-5,100))
plt.yscale('log')
plt.ylabel('Runtime (s)')
# Create legend & Show graphic
plt.title(loaddata)
plt.legend()
plt.show()


