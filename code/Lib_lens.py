#Author: Martín Manuel Gómez Míguez
#GitHub: @Correlo
#Date: 03/04/2020

import numpy as np

def gcirc(n,  rad, rc = (0.0, 0.0)):
    '''
    Input
    
    n   -> number of pixels along one axis (Einstein radius)
    rad -> sigma (Einstein radius)
    rc  -> position of the center (Einstein radius)
    
    Output
    
    I   -> Gaussian intensity
    '''
    #Create mesh
    x, y = np.mgrid[0:n, 0:n]
    #Square of the distance (pay attention to y-matrix)
    r2 = (y - rc[0] - n/2)**2 + (x - rc[1] - n/2)**2
    #Exponential of the intensity
    a = np.exp(- r2*0.5/rad**2)
    #Normalization (A = 1)
    I = a/a.sum()
    
    return I

def Identity(X1, X2, LENS):
    '''
    Input
    
    X1 -> x coordinate of image space (Einstein radius)
    X2 -> y coordinate of image space (Einstein radius)
    
    Output
    
    Alpha1 -> x coordinate of deflection (Einstein radius)
    Alpha2 -> y coordinate of deflection (Einstein radius)
    '''
    
    Alpha1, Alpha2 = 0., 0.
    
    return [Alpha1, Alpha2]

def PSL(X1, X2, LENS):
    '''
    Input

    X1 -> x coordinate of image space (Einstein radius)
    X2 -> y coordinate of image space (Einstein radius)
    rl -> position of the center (Einstein radius)
    ml -> lens mass

    Output

    Alpha1 -> x coordinate of deflection (Einstein radius)
    Alpha2 -> y coordinate of deflection (Einstein radius)
    '''
    param_l = list(dict(LENS).keys())[1:]
    rx = [float(LENS[x]) for x in param_l if 'x' in x]
    ry = [float(LENS[y]) for y in param_l if 'y' in y]
    rl = [(x, y) for x,y in zip(rx,ry)]
    ml = [float(LENS[m]) for m in param_l if 'ml' in m]
    
    if (len(ml) != len(rl)): raise ValueError('Las masas y centros de las lentes no han sido asignados correctamente.')

    Alpha1, Alpha2 = 0., 0.
    for i in range(len(ml)):
  
        #Square of the distance
        d2 = (X1 - rl[i][0])**2 + (X2 + rl[i][1])**2 + 1e-12 #Correction to avoid divergence
        #Deflection
        alpha1, alpha2 = ml[i]*(X1 - rl[i][0])/d2, ml[i]*(X2 + rl[i][1])/d2
        Alpha1 += alpha1; Alpha2 += alpha2

    return [Alpha1, Alpha2]
              
def ChangRefsdal(X1, X2, LENS):
    '''
    Input

    X1 -> x coordinate of image space (Einstein radius)
    X2 -> y coordinate of image space (Einstein radius)
    rl -> position of the center (Einstein radius)
    ml -> lens mass
    k  -> convergence
    g  -> shear

    Output

    Alpha1 -> x coordinate of deflection (Einstein radius)
    Alpha2 -> y coordinate of deflection (Einstein radius)
    '''
    param_l = list(dict(LENS).keys())[1:]
    rx = [float(LENS[x]) for x in param_l if 'x' in x]
    ry = [float(LENS[y]) for y in param_l if 'y' in y]
    rl = [(x, y) for x,y in zip(rx, ry)]
    ml = [float(LENS[m]) for m in param_l if 'ml' in m]
    k  = float(LENS['k'])
    g  = float(LENS['g'])

    if (len(ml) != len(rl)): raise ValueError('Las masas y centros de las lentes no han sido asignados correctamente.')
    if ((k > 1) or (k < 0) or (g > 1) or (g < 0)): raise ValueError('Revise el rango de valores de los parametros')

    #Background effect
    Alpha1, Alpha2 = (k + g)*X1, (k - g)*X2
    for i in range(len(ml)):

        #Square of the distance
        d2 = (X1 - rl[i][0])**2 + (X2 + rl[i][1])**2 + 1e-12 #Correction to avoid divergence
        #Deflection
        alpha1, alpha2 = ml[i]*(X1 - rl[i][0])/d2, ml[i]*(X2 + rl[i][1])/d2
        Alpha1 += alpha1; Alpha2 += alpha2

    return [Alpha1, Alpha2]

def SIS(X1, X2, LENS):
    '''
    Input
    
    X1 -> x coordinate of image space (Einstein radius)
    X2 -> y coordinate of image space (Einstein radius)
    rl -> position of the center (Einstein radius)
    ThE -> Einstein radius
    
    Output
    
    Alpha1 -> x coordinate of deflection (Einstein radius)
    Alpha2 -> y coordinate of deflection (Einstein radius)
    '''
    rx = float(LENS['rlx'])
    ry = float(LENS['rly'])
    rl = (rx, ry)
    ThE = float(LENS['ThE'])

    #Square of the distance
    d = np.sqrt((X1 - rl[0])**2 + (X2 + rl[1])**2 + 1e-12) #Correction to avoid divergence
    #Deflection
    Alpha1, Alpha2 = ThE*(X1 - rl[0])/d, ThE*(X2 + rl[1])/d

    return [Alpha1, Alpha2]


def select_lens(mode):
    
    if mode == 'Identity': return lambda X1, X2, LENS : Identity(X1, X2, LENS)

    if mode == 'PSL': return lambda X1, X2, LENS: PSL(X1, X2, LENS)
                      
    if mode == 'ChangRefsdal': return lambda X1, X2, LENS : ChangRefsdal(X1, X2, LENS)
    
    if mode == 'SIS': return lambda X1, X2, LENS : SIS(X1, X2, LENS)

    else: raise ValueError('El modo seleccionado no existe o no se encuentra disponible.')






