#Author: Martín Manuel Gómez Míguez
#GitHub: @Correlo
#Date: 03/04/2020

from configparser import ConfigParser

#Modules of the developer
from Core import Core

#Read params.ini
params = ConfigParser()
params.sections()
params.read('params.ini')

#List of fields
fields = list(dict(params).keys())
#List of lenses
lenses = [elem for elem in fields if elem[0] == 'L']

#Main parte of the code
for lens in lenses:
    print()
    print('Obtaining ', lens)
    Core(params, lens)

print()
print('All the lenses were created successfully!')


