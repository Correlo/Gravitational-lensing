#Author: Martín Manuel Gómez Míguez
#GitHub: @Correlo
#Date: 08/02/2020

from configparser import ConfigParser

#Modules of the developer
from Core import Core

#Read params.ini
params = ConfigParser()
params.sections()
params.read('params.ini')

#Labels
MESH = params['MESH']
SOURCE = params['SOURCE']
LENS_l = list(dict(params).keys())[3:]

#Main parte of the code
for i in range(len(LENS_l)):
    LENS = params[LENS_l[i]]
    figname = 'Lens' + str(i) + '.png'
    print('Obtaining ', figname)
    Core(MESH, SOURCE, LENS, figname)

print()
print('All the lens was created successfully!')


