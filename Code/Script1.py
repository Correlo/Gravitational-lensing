#Author: Martín Manuel Gómez Míguez
#GitHub: @Correlo
#Date: 08/02/2020

import numpy as np
import matplotlib.pyplot as plt
import Source as s

#Mesh parameters
nX = 401 # Number of pixels in image plane
nY = 401 # Number of pixels in source plane

# Plane dimensions in 'Einstein' radius
XL = 2.  # Half size of the image plane covered
YL = 2.  # Half size of the source plane covered

''' Check if is nX or nX - 1 '''
Xl = 2.*XL/nX # pixel size on the image map
Yl = 2.*YL/nY # pixel size on the source map

#Source parameters in 'Einstein' radius
rs = (0.0, 1.0) # Source position
rad = 0.1 # Source radius

#From Einstein radius to pixel position
rsp = (int(round(rs[0]/Yl)), int(round(rs[1]/Yl)))
radp = int(round(rad/Yl))

#Obtain the normalized intensity of the source
IY = s.gcirc(nY,  radp, rsp)

#Create an empty image intensity field
IX = np.zeros((nX, nY))

#Create mesh
X2p, X1p = np.mgrid[0:nX, 0:nX]
#From pixel to 'Einstein' radius
X1, X2 = -XL + X1p*Xl, -XL + X2p*Xl
#Deflection using Inverse Ray Shooting (Identity transformation)
Y1, Y2 = X1 - 0., X2 - 0.
#From 'Einstein' radius to pixel position
Y1p, Y2p = np.round((Y1 + YL)/Yl).astype('int'), np.round((Y2 + YL)/Yl).astype('int')
#Check that the obtained pixel index is inside bounds
Y1in, Y2in = np.where((Y1p > 0) & (Y1p < nY)), np.where((Y2p > 0) & (Y2p < nY))
#Obtain the image plane
IX[X1p[Y1in], X2p[Y2in]] = IY[Y1p[Y1in], Y2p[Y2in]]

#Plot the results
fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (12, 6))
ax1.set_title('Source plane', fontsize = 15)
im1 = ax1.imshow(IY, extent = (-YL, YL, -YL, YL), origin = 'lower')
fig.colorbar(im1, ax = ax1, fraction=0.046, pad=0.04).ax.set_ylabel('I', fontsize = 12)
ax1.set_xlabel('X (Einstein radius)', fontsize = 12)
ax1.set_ylabel('Y (Einstein radius)', fontsize = 12)

ax2.set_title('Image plane', fontsize = 15)
im2 = ax2.imshow(IX, extent = (-XL, XL, -XL, XL), origin = 'lower')
fig.colorbar(im2, ax = ax2, fraction=0.046, pad=0.04).ax.set_ylabel('I', fontsize = 12)
ax2.set_xlabel('X (Einstein radius)', fontsize = 12)
ax2.set_ylabel('Y (Einstein radius)', fontsize = 12)

plt.subplots_adjust(wspace = 0.5)

plt.savefig('Identity')



