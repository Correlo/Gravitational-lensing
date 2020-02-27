#Author: Martín Manuel Gómez Míguez
#GitHub: @Correlo
#Date: 08/02/2020

import numpy as np
import matplotlib.pyplot as plt
from configparser import ConfigParser

#Modules of the developer
import Lib_lens as Ll

def Core(MESH, SOURCE, LENS, figname):
    
    ''' Mesh '''
    #Mesh parameters
    nX = int(MESH['nX']) # Number of pixels in image plane
    nY = int(MESH['nY']) # Number of pixels in source plane

    #Plane dimensions in 'Einstein' radius
    XL = float(MESH['XL']) # Half size of the image plane covered
    YL = float(MESH['YL']) # Half size of the source plane covered

    ''' Source '''
    #Source parameters in 'Einstein' radius
    rs = (float(SOURCE['rsx']), float(SOURCE['rsy'])) # Source position
    rad = float(SOURCE['rad']) # Source radius
    
    ''' Deflection '''
    deflect = Ll.select_lens(LENS['mode'])
    
    #Center of the pixel
    Xl = 2.*XL/(nX - 1) # pixel size on the image map
    Yl = 2.*YL/(nY - 1) # pixel size on the source map
    
    #From Einstein radius to pixel position
    rsp = (int(round(rs[0]/Yl)), -int(round(rs[1]/Yl)))
    radp = int(round(rad/Yl))
    
    #Obtain the normalized intensity of the source
    IY = Ll.gcirc(nY,  radp, rsp)

    #Create an empty image intensity field
    IX = np.zeros((nX, nX))
    
    for X2p in range(nX):
        for X1p in range(nX):
            X1, X2 = -XL + X2p*Xl, -XL + X1p*Xl # From pixels to Einstein radius
            alpha1, alpha2 = 0., 0. # Identity
            alpha1, alpha2 = deflect(X1, X2, LENS)
            
            #Deflection using Inverse Ray Shooting
            Y1, Y2 = X1 - alpha1, X2 - alpha2
            #From 'Einstein' radius to pixel position
            Y2p, Y1p = int(np.round((Y1 + YL)/Yl)), int(np.round((Y2 + YL)/Yl))
            #Check that the obtained pixel index is inside bounds
            if ((Y1p >= 0) & (Y1p < nY) & (Y2p >= 0) & (Y2p < nY)):
                #Obtain the image plane
                IX[X1p, X2p] = IY[Y1p, Y2p]

    #Plot the results
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (12, 6))
    ax1.set_title('Source plane', fontsize = 15)
    im1 = ax1.imshow(IY, extent = (-YL, YL, -YL, YL))
    fig.colorbar(im1, ax = ax1, fraction = 0.046, pad = 0.04).ax.set_ylabel('I', fontsize = 12)
    ax1.set_xlabel(r'X ($\theta_E$)', fontsize = 12)
    ax1.set_ylabel(r'Y ($\theta_E$)', fontsize = 12)

    ax2.set_title('Image plane', fontsize = 15)
    im2 = ax2.imshow(IX, extent = (-XL, XL, -XL, XL))
    fig.colorbar(im2, ax = ax2, fraction = 0.046, pad = 0.04).ax.set_ylabel('I', fontsize = 12)
    ax2.set_xlabel(r'X ($\theta_E$)', fontsize = 12)
    ax2.set_ylabel(r'Y ($\theta_E$)', fontsize = 12)

    plt.subplots_adjust(wspace = 0.5)

    plt.savefig(figname)




