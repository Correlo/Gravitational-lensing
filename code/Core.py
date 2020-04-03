#Author: Martín Manuel Gómez Míguez
#GitHub: @Correlo
#Date: 03/04/2020

import numpy as np
import matplotlib.pyplot as plt
from configparser import ConfigParser
from PIL import Image
from os.path import isdir
from os import mkdir

#Modules of the developer
import Lib_lens as Ll

def Core(params, lens):
    
    #List of fields
    fields = list(dict(params).keys())
    
    #Initializate some parameters
    nX, nY, XL, YL, Xl, Yl, IY = 0, 0, 0, 0, 0, 0, 0
    #Configure parameters
    if 'IMAGE' in fields:
        
        IMAGE = params['IMAGE']
        
        print('Reading %s ...' % IMAGE['path'])
        
        #Open image
        im = Image.open(IMAGE['path'])
        Im = np.array(im)
        
        #Mesh parameters. Mesh must be square
        Dim = Im.shape
        nY = min(Dim[0], Dim[1]) # Select a square
        nY -= nX % 2 # even value for nX
        nX = nY
    
        #Plane dimensions in arbitrary units
        XL = float(IMAGE['XL'])
        YL = float(IMAGE['YL'])
    
        #Center of the pixel
        Xl = 2.*XL/(nX - 1) # pixel size on the image map
        Yl = 2.*YL/(nY - 1) # pixel size on the source map
        
        #Obtain the flux of the source
        IY = Im[:nY, :nY, :]
    
    elif ('MESH' in fields) and ('SOURCE' in fields):
        
        MESH = params['MESH']
        SOURCE = params['SOURCE']
        
        ''' Mesh '''
        print('Creating mesh ...')
        #Mesh parameters. Mesh must be square
        nX = int(MESH['nX']) # Number of pixels in image plane
        nY = int(MESH['nY']) # Number of pixels in source plane

        #Plane dimensions in 'Einstein' radius
        XL = float(MESH['XL']) # Half size of the image plane covered
        YL = float(MESH['YL']) # Half size of the source plane covered

        ''' Source '''
        print('Preparing the Gaussian source ...')
        #Source parameters in 'Einstein' radius
        rs = (float(SOURCE['rsx']), float(SOURCE['rsy'])) # Source position
        rad = float(SOURCE['rad']) # Source radius
    
        #Center of the pixel
        Xl = 2.*XL/(nX - 1) # pixel size on the image map
        Yl = 2.*YL/(nY - 1) # pixel size on the source map
    
        #From Einstein radius to pixel position
        rsp = (int(round(rs[0]/Yl)), -int(round(rs[1]/Yl)))
        radp = int(round(rad/Yl))
    
        #Obtain the normalized intensity of the source
        IY = Ll.gcirc(nY, radp, rsp)
    
    else: raise ValueError('Alguno de los campos de configuración falta o los dados no son validos.')
    
    ''' Deflection mode '''
    LENS = params[lens]
    #Deflect function
    deflect = Ll.select_lens(LENS['mode'])
    print('Selecting %s lens' % LENS['mode'])

    ''' Magnification map '''
    if int(LENS['mag']) == 1:
        
        print('Obtaining magnification map ...')
        raypix = float(LENS['rp'])     # Number of rays per pixel
        Xl_m = Yl/np.sqrt(raypix) # Side of the transported area
        XL_m = 2*YL               # Size of the shooting region at the image plane
        # Size definition is arbitrary
        
        nX_m = np.round(2*XL_m/Xl_m) + 1 # Number of rays on a column/row at the image plane
        
        Xrp = np.arange(nX_m) # Array with pixels on y direction
        X2p_m, X1p_m = np.mgrid[0:1, 0:nX_m] # Grid with pixel coordinates for a row at the image
        
        #Initialize magnification map
        Mag = np.zeros((nY, nY))
        
        perc0 = 5. # Percentage step for printing progress
        perc = 5.  # Initial value for perc
        
        #Loop
        for i in Xrp:
            
            if ((i*100/nX_m) >= perc): # Check if we have already completed perc.
                perc += perc0 # Increase perc.
                print(round(i*100/nX_m)) # Print progress
        
            X1, X2 = - XL_m + X2p_m*Xl_m, - XL_m + X1p_m*Xl_m # Convert pixels to coordinates in the image plane
            
            #Deflection
            alpha1, alpha2 = deflect(X1, X2, LENS)
            Y1, Y2 = X1 - alpha1, X2 - alpha2
            Y1p, Y2p = ((Y1 + YL)/Yl).astype('int'), ((Y2 + YL)/Yl).astype('int')
            
            #Index that we need
            i_bool = (Y1p >= 0) & (Y1p < nY) & (Y2p >= 0) & (Y2p < nY)
            
            Y1p_in, Y2p_in = Y1p[i_bool], Y2p[i_bool]
            
            for i in range(len(Y1p_in)):
                
                Mag[Y2p_in[i], Y1p_in[i]] += 1 # Increase magnification at those pixels
    
            X2p_m += 1.0 # Continue qith the following row
                    
        #Normalization
        Mag = Mag/raypix
        plt.close()
        fig, ax0 = plt.subplots(figsize = (6, 6))
        im = plt.imshow(Mag, vmin = 0, vmax = raypix, extent = (-YL, YL, -YL, YL))
        fig.colorbar(im, ax = ax0, fraction = 0.046, pad = 0.04)
        ax0.set_xlabel(r'X ($\theta_E$)', fontsize = 12)
        ax0.set_ylabel(r'Y ($\theta_E$)', fontsize = 12)
        
        
        Outdir = 'Figures/'
        if not isdir(Outdir): mkdir(Outdir)
        
        Outmagdir = Outdir + 'Mag/'
        if not isdir(Outmagdir): mkdir(Outmagdir)
        
        plt.savefig(Outmagdir + lens + '.png')
        np.save(Outmagdir + lens + '.npy', Mag)

        print('Results saved in %s' % Outmagdir)
        
    ''' Deflection '''
    #Create an empty image intensity field
    IX = np.zeros_like(IY)

    print('Deflecting source image ...')
    for X2p in range(nX):
        for X1p in range(nX):
            X1, X2 = -XL + X2p*Xl, -XL + X1p*Xl # From pixels to Einstein radius
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
    if 'IMAGE' in fields:
        
        im = Image.fromarray(IY)
        im_out = Image.fromarray(IX)

        #Plot the results
        plt.close()
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (12, 6))
        ax1.set_title('Source plane', fontsize = 15)
        ax1.imshow(im)
        ax1.set_axis_off()

        ax2.set_title('Image plane', fontsize = 15)
        ax2.imshow(im_out)
        ax2.set_axis_off()

        plt.subplots_adjust(wspace = 0.1)

        Outdir = 'Figures/'
        if not isdir(Outdir): mkdir(Outdir)
        
        Outfigdir = Outdir + 'Compare/'
        if not isdir(Outfigdir): mkdir(Outfigdir)
        
        plt.savefig(Outfigdir + lens + '.png')
    
        #Save .tiff image
        Outmoddir = Outdir + 'Mod/'
        if not isdir(Outmoddir): mkdir(Outmoddir)
        im_out.save(Outmoddir + lens + '.tiff')

        print('Results saved in %s' % Outmoddir)

    elif ('MESH' in fields) and ('SOURCE' in fields):

        plt.close()
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (12, 6))
        ax1.set_title('Source plane', fontsize = 15)
        im1 = ax1.imshow(IY, extent = (-YL, YL, -YL, YL))
        fig.colorbar(im1, ax = ax1, fraction = 0.046, pad = 0.04)
        ax1.set_xlabel(r'X ($\theta_E$)', fontsize = 12)
        ax1.set_ylabel(r'Y ($\theta_E$)', fontsize = 12)

        
        ax2.set_title('Image plane', fontsize = 15)
        im2 = ax2.imshow(IX, extent = (-XL, XL, -XL, XL))
        fig.colorbar(im2, ax = ax2, fraction = 0.046, pad = 0.04)
        ax2.set_xlabel(r'X ($\theta_E$)', fontsize = 12)
        ax2.set_ylabel(r'Y ($\theta_E$)', fontsize = 12)

        plt.subplots_adjust(wspace = 0.5)
        
        Outdir = 'Figures/'
        if not isdir(Outdir): mkdir(Outdir)
        
        Outfigdir = Outdir + 'Compare/'
        if not isdir(Outfigdir): mkdir(Outfigdir)

        plt.savefig(Outfigdir + lens + '.png')
        
        print('Results saved in %s' % Outfigdir)

        Outmoddir = Outdir + 'Mod/'
        if not isdir(Outmoddir): mkdir(Outmoddir)
        np.save(Outmoddir + lens + '.npy', IX)

        print('Results saved in %s' % Outmoddir)

    else: raise ValueError('Alguno de los campos de configuración falta o los dados no son validos.')






