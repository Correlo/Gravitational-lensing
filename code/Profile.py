#Author: Martín Manuel Gómez Míguez
#GitHub: @Correlo
#Date: 03/04/2020

import numpy as np
import matplotlib.pyplot as plt
from os.path import isfile, isdir
from os import mkdir
from scipy.signal import fftconvolve

#Modules of the developer
import Lib_lens as Ll

''' Parameters '''

#Name of the magnification map file
LFile = 'Figures/Mag/LENS3.npy'

p0 = (0, 0)
p1 = (401, 401)

YL = 2. # Half size of the source plane covered
rp = 16 # Number of rays per pixel

#Gaussian source parameters in 'Einstein' radius
rad = [0.05, 0.1, 0.2, 0.5] # Source radius

Outname = 'Prof1.png' # Output filename


''' Code '''

def profile(data, p0, p1):

    '''
    Input
    
    data -> 2D-array
    p0   -> tuple with pixel coordinates of the initial point
    p1   -> tuple with pixel coordinates of the ending point
    
    Output
    
    prof -> array with the desired profile
    '''

    #Length of track in pixels
    num = int(round(np.sqrt((p1[0] - p0[0])**2 + (p1[1] - p0[1])**2)))
    # Pixel coordinates of the profile pixels
    Y1p, Y2p = np.linspace(p0[0], p1[0], num), np.linspace(p0[1], p1[1], num)
    Y1p, Y2p = Y1p.astype('int'), Y2p.astype('int')

    #Obtain the profile
    prof = data[Y2p, Y1p]

    return [Y1p, Y2p, prof]


#Check if LFile exists
if not isfile(LFile): raise ValueError('El fichero indicado no existe.')
Mag = np.load(LFile)

nY = Mag.shape[0]   # Number of pixels per axis in source plane
Yl = 2.*YL/(nY - 1) # pixel size on the source map

#Obtain the profile
Y1p, Y2p, prof = profile(Mag, p0, p1)
Y = np.sign(-YL + Y1p*Yl)*np.sqrt((-YL + Y1p*Yl)**2 + (-YL + Y2p*Yl)**2)

# Highlight profile line
Mag[Y2p, Y1p] = rp

#Lists to store measured data
MAG = [Mag]
PROF = [prof]

for i in range(len(rad)):

    #From Einstein radius to pixel position
    radp = int(round(rad[i]/Yl))

    #Obtain the normalized intensity of the source
    IY = Ll.gcirc(nY, radp)

    #Convolution
    Mag_eff = fftconvolve(IY, Mag, mode = 'same')

    #Profile
    _, _, prof = profile(Mag_eff, p0, p1)

    #Save data
    MAG.append(Mag_eff)
    PROF.append(prof)


#Plot results
plt.close()
fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (12, 6))
ax1.set_title('Magnification field', fontsize = 15)
im1 = ax1.imshow(MAG[0], vmin = 0, vmax = rp, extent = (-YL, YL, -YL, YL))
fig.colorbar(im1, ax = ax1, fraction = 0.046, pad = 0.04)
ax1.set_xlabel(r'X ($\theta_E$)', fontsize = 12)
ax1.set_ylabel(r'Y ($\theta_E$)', fontsize = 12)

ax2.set_title('Profile', fontsize = 15)
ax2.plot(Y, PROF[0], 'k-', label = 'Uniform source')
for i in range(len(PROF) - 1):  ax2.plot(Y, PROF[i + 1], '-', label = 'rad = %.2f ' % rad[i])
ax2.set_xlabel(r'X ($\theta_E$)', fontsize = 12)
ax2.set_xlim(min(Y), max(Y))
ax2.set_ylabel(r'Magnification (ADU)', fontsize = 12)
ax2.legend(frameon = False)

plt.subplots_adjust(wspace = 0.25)
plt.tight_layout()

Outdir = 'Figures/'
if not isdir(Outdir): mkdir(Outdir)

Outprofdir = Outdir + 'Profile/'
if not isdir(Outprofdir): mkdir(Outprofdir)

plt.savefig(Outprofdir + Outname)




