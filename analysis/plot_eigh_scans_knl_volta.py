 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 19:36:15 2019

@author: stephey
"""
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import pickle

matplotlib.rcParams['axes.linewidth'] = 1.5 #set the value globally


#plot eigh scans
msizes = [100, 500, 1000, 5000, 10000, 15000]
mdivs = [1,2,5,10]

#what do you want to load
#loaddata = 'skylake'
#loaddata = 'volta'
#loaddata = 'haswell'
loaddata = 'knl'
loadstring = '/Users/stephey/Dropbox/NERSC/Work/Dates/20190522/eigh_' + str(loaddata) + '.pickle'

#should load mdiv_data
with open(loadstring, 'rb') as handle:
    nresults_knl = pickle.load(handle)
    

#throw away the first trial...

#get mean and std but throw away first trial
nresults_knl_mean = np.mean(nresults_knl[1:,:,:], axis=0)

loaddata = 'volta'
loadstring = '/Users/stephey/Dropbox/NERSC/Work/Dates/20190522/eigh_' + str(loaddata) + '.pickle'

#should load mdiv_data
with open(loadstring, 'rb') as handle:
    nresults_volta = pickle.load(handle)
    

#throw away the first trial...

#get mean and std but throw away first trial
nresults_volta_mean = np.mean(nresults_volta[1:,:,:], axis=0)

#also haswell?

loaddata = 'haswell'
loadstring = '/Users/stephey/Dropbox/NERSC/Work/Dates/20190522/eigh_' + str(loaddata) + '.pickle'

#should load mdiv_data
with open(loadstring, 'rb') as handle:
    nresults_haswell = pickle.load(handle)

#get mean and std but throw away first trial
nresults_haswell_mean = np.mean(nresults_haswell[1:,:,:], axis=0)



#transparency 
alpha=0.3
 
# Make the plot
plt.figure()
plt.plot(msizes, nresults_knl_mean[:,0], color='red', linestyle='solid', label='knl mdiv 1')
plt.plot(msizes, nresults_knl_mean[:,1], color='red', linestyle='dashdot', label='knl mdiv 2')
plt.plot(msizes, nresults_knl_mean[:,2], color='red', linestyle='dashed', label='knl mdiv 5')
plt.plot(msizes, nresults_knl_mean[:,3], color='red', linestyle='dotted', label='knl mdiv 10')
plt.plot(msizes, nresults_haswell_mean[:,0], color='green', linestyle='solid', label='haswell mdiv 1')
plt.plot(msizes, nresults_haswell_mean[:,1], color='green', linestyle='dashdot', label='haswell mdiv 2')
plt.plot(msizes, nresults_haswell_mean[:,2], color='green', linestyle='dashed', label='haswell mdiv 5')
plt.plot(msizes, nresults_haswell_mean[:,3], color='green', linestyle='dotted', label='haswell mdiv 10')
plt.plot(msizes, nresults_volta_mean[:,0], color='blue', linestyle='solid', label='volta mdiv 1')
plt.plot(msizes, nresults_volta_mean[:,1], color='blue', linestyle='dashdot', label='volta mdiv 2')
plt.plot(msizes, nresults_volta_mean[:,2], color='blue', linestyle='dashed', label='volta mdiv 5')
plt.plot(msizes, nresults_volta_mean[:,3], color='blue', linestyle='dotted', label='volta mdiv 10')
plt.fill_between(msizes, nresults_knl_mean[:,0],nresults_knl_mean[:,3], color='red', alpha=alpha)
plt.fill_between(msizes, nresults_haswell_mean[:,0],nresults_haswell_mean[:,3], color='green', alpha=alpha)
plt.fill_between(msizes, nresults_volta_mean[:,0],nresults_volta_mean[:,3], color='blue', alpha=alpha)

plt.yscale('log')
plt.xscale('log')
plt.ylabel('Runtime (s)')
plt.xlabel('Matrix size')
# Create legend & Show graphic
plt.legend(loc='top right')
plt.show()

# Make the plot
plt.figure()
plt.plot(msizes, nresults_knl_mean[:,0]/msizes, color='red', linestyle='solid', label='knl mdiv 1')
plt.plot(msizes, nresults_knl_mean[:,1]/msizes, color='red', linestyle='dashdot', label='knl mdiv 2')
plt.plot(msizes, nresults_knl_mean[:,2]/msizes, color='red', linestyle='dashed', label='knl mdiv 5')
plt.plot(msizes, nresults_knl_mean[:,3]/msizes, color='red', linestyle='dotted', label='knl mdiv 10')
plt.plot(msizes, nresults_haswell_mean[:,0]/msizes, color='green', linestyle='solid', label='haswell mdiv 1')
plt.plot(msizes, nresults_haswell_mean[:,1]/msizes, color='green', linestyle='dashdot', label='haswell mdiv 2')
plt.plot(msizes, nresults_haswell_mean[:,2]/msizes, color='green', linestyle='dashed', label='haswell mdiv 5')
plt.plot(msizes, nresults_haswell_mean[:,3]/msizes, color='green', linestyle='dotted', label='haswell mdiv 10')
plt.plot(msizes, nresults_volta_mean[:,0]/msizes, color='blue', linestyle='solid', label='volta mdiv 1')
plt.plot(msizes, nresults_volta_mean[:,1]/msizes, color='blue', linestyle='dashdot', label='volta mdiv 2')
plt.plot(msizes, nresults_volta_mean[:,2]/msizes, color='blue', linestyle='dashed', label='volta mdiv 5')
plt.plot(msizes, nresults_volta_mean[:,3]/msizes, color='blue', linestyle='dotted', label='volta mdiv 10')
plt.fill_between(msizes, nresults_knl_mean[:,0]/msizes,nresults_knl_mean[:,3]/msizes, color='red', alpha=alpha)
plt.fill_between(msizes, nresults_haswell_mean[:,0]/msizes,nresults_haswell_mean[:,3]/msizes, color='green', alpha=alpha)
plt.fill_between(msizes, nresults_volta_mean[:,0]/msizes,nresults_volta_mean[:,3]/msizes, color='blue', alpha=alpha)
plt.yscale('log')
plt.xscale('log')
plt.ylabel('Runtime (s)/ Matrix Size')
plt.xlabel('Matrix size')
# Create legend & Show graphic
plt.legend(loc='top right')
plt.show()

# Make the plot
plt.figure()
plt.plot(msizes, nresults_haswell_mean[:,0], color='blue', linestyle='solid', label='Cori Haswell', linewidth=1.5)
plt.plot(msizes, nresults_knl_mean[:,0], color='green', linestyle='solid', label='Cori KNL', linewidth=1.5)
plt.plot(msizes, nresults_volta_mean[:,0], color='red', linestyle='solid', label='Cori Volta', linewidth=1.5)

plt.tick_params(axis='both', which='major', labelsize=14)
plt.tick_params(axis='both', which='minor', labelsize=8)

plt.yscale('log')
plt.xscale('log')
plt.ylabel('Runtime (s)', fontsize=14)
plt.xlabel('Size of eigh matrix', fontsize=14)
# Create legend & Show graphic
leg = plt.legend(fontsize=14)

leg.get_frame().set_linewidth(1.5)
leg.get_frame().set_edgecolor("k")

plt.tight_layout()
plt.show()
