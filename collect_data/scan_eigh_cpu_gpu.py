#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 16:16:34 2019

@author: stephey
"""

"""
Created on Fri Apr 26 12:07:11 2019

@author: stephey
"""

#try testing eigh on gpu with cupy

import numpy as np
import cupy as cp
from scipy import random, linalg
import time
import pickle

# =============================================================================
# import argparse
# parser = argparse.ArgumentParser(description='input for eigh testing')
# parser.add_argument('--dim', type=int, action='store', default=100,
#                     help='dimension of matrix')
# parser.add_argument('--slices', type=int, action='store', default=1,
#                     help='number of matrix slices')
# 
# args = parser.parse_args()
# N = args.dim
# m = args.slices
# =============================================================================

#read in pre-created matrices
N100 = np.load('N100.npy')
N500 = np.load('N500.npy')
N1000 = np.load('N1000.npy')
N5000 = np.load('N5000.npy')
N10000 = np.load('N10000.npy')
N15000 = np.load('N15000.npy')

matrix_list = ['N100', 'N500', 'N1000', 'N5000', 'N10000', 'N15000']
#matrix_list = ['N100', 'N500', 'N1000']
nmatrices = len(matrix_list)

mdiv = [1,2,5,10]
ndiv = len(mdiv)

ntrials = 6

#preallocate numpy matrix (and later cupy matrix)
#to stick in timer data
nresults = np.zeros([ntrials,nmatrices,ndiv])

#loop over matrix sizes
for i in range(nmatrices):
    mat = eval(matrix_list[i]) #dangerous but hopefully ok
    mat_size = mat.shape[0]

    #how many time trials
    for z in range(ntrials):
        #then divide each matrix into mdiv pieces
        #time total of all pieces
        for j, div in enumerate(mdiv):
            #how big is each piece?
            block_size = mat_size // div
            #and do however many pieces
            ibox = block_size
            istart = 0
            #start new every time
            eigh_time_mdiv = list()
            for m in range(div):
                #let's do the whole matrix just to be consistent
                iend = istart + ibox
                box = np.copy(mat[istart:iend,istart:iend])
                #check if this is a view -- no
                #print(box.base)
                eigh_start = time.time()
                eigh = np.linalg.eigh(box)
                eigh_end = time.time()
                istart = istart + ibox
                eigh_time_mdiv.append(eigh_end - eigh_start)
            #sum all times for mdiv
            mdiv_sum = np.sum(eigh_time_mdiv)
            print("cpu trial %s mat size %s mdiv %s mdiv sum %s" %(z,mat_size,div,mdiv_sum))
            nresults[z,i,j] = mdiv_sum


#save data to pickle file
with open('eigh_cpu.pickle', 'wb') as handle:
    pickle.dump(nresults, handle, protocol=pickle.HIGHEST_PROTOCOL)


#preallocate numpy matrix (and later cupy matrix)
#to stick in timer data
nresults= np.zeros([ntrials,nmatrices,ndiv])
#move to device
nresults_gpu = cp.array(nresults)

#and now move the data to the gpu
N100_gpu = cp.array(N100)
N500_gpu = cp.array(N500)
N1000_gpu = cp.array(N1000)
N5000_gpu = cp.array(N5000)
N10000_gpu = cp.array(N10000)
N15000_gpu = cp.array(N15000)

matrix_list = ['N100_gpu', 'N500_gpu', 'N1000_gpu', 'N5000_gpu', 'N10000_gpu', 'N15000_gpu']
#matrix_list = ['N100_gpu', 'N500_gpu', 'N1000_gpu']
nmatrices = len(matrix_list)

#loop over matrix sizes
for i in range(nmatrices):
    mat = eval(matrix_list[i]) #dangerous but hopefully ok
    mat_size = mat.shape[0]

    #how many time trials
    for z in range(ntrials):
        #then divide each matrix into mdiv pieces
        #time total of all pieces
        for j, div in enumerate(mdiv):
            #how big is each piece?
            block_size = mat_size // div
            #and do however many pieces
            ibox = block_size
            istart = 0
            #start new every time
            eigh_time_mdiv = list()
            for m in range(div):
                #let's do the whole matrix just to be consistent
                iend = istart + ibox
                box = cp.copy(mat[istart:iend,istart:iend])
                #check if this is a view -- no
                #print(box.base)
                eigh_start = time.time()
                eigh = cp.linalg.eigh(box)
                eigh_end = time.time()
                istart = istart + ibox
                eigh_time_mdiv.append(eigh_end - eigh_start)
                eigh_time_mdiv_array = cp.array(eigh_time_mdiv)
            #sum all times for mdiv
            mdiv_sum = cp.sum(eigh_time_mdiv_array)
            print("gpu trial %s mat size %s mdiv %s mdiv sum %s" %(z,mat_size,div,mdiv_sum))
            nresults_gpu[z,i,j] = mdiv_sum


#now bring the data back to the host
nresults = nresults_gpu.get()

#save data to pickle file
with open('eigh_gpu.pickle', 'wb') as handle:
    pickle.dump(nresults, handle, protocol=pickle.HIGHEST_PROTOCOL)


