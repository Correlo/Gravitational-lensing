#Author: Martín Manuel Gómez Míguez
#GitHub: @Correlo
#Date: 08/02/2020

import numpy as np

def gcirc(n,  rad, rc = (0.0, 0.0)):
    '''
    Input
    
    n   -> number of pixels along one axis
    rad -> sigma
    rc  -> position of the center
    
    Output
    
    I   -> Gaussian intensity
    '''
    #Create mesh
    y, x = np.mgrid[0:n, 0:n]
    #Square of the distance (pay attention to y-matrix)
    r2 = (x - rc[0] - n/2)**2 + (y - rc[1] - n/2)**2
    #Exponential of the intensity
    a = np.exp(- r2*0.5/rad**2)
    #Normalization (A = 1)
    I = a/a.sum()

    return I
