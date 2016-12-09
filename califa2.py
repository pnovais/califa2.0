'''
Programa para trabalhar os dados do CALIFA
Uma nova abordagem, sem separacao de populacoes estelares
Retomando minha pesquisa... Que o Universo me ajude!

07-dezembro-2016
'''

#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime
import time
from sys import exit
from matplotlib import colors, pyplot as plt
from functools import reduce
import matplotlib.cm as cm
import seaborn as sns
from astropy.io import ascii, fits
from astropy.wcs import wcs
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from scipy.interpolate import interp2d
import cubehelix
import matplotlib.mlab as mlab
import scipy, pylab
import math

__author__ = 'pnovais'
ini=time.time()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    PATY = '\033[32m'
    PINK = '\033[35m'
    YELLOWs = '\033[33m'


#definindo a classe que ira ler as imagens fits
def get_image(f_sdss):
    img = f_sdss[0].data
#    sky = f_sdss[2].data
    return img

data_dir = '/home/pnovais/Dropbox/DOUTORADO/renew'
age = pd.read_csv('Paty_at_flux__yx/age.csv')
mass = pd.read_csv('PatImages/mass.csv')
halpha = pd.read_csv('Hamaps/halpha.csv')


for i_gal in range(len(halpha)):
#for i_gal in range(0,3):
    print(bcolors.FAIL +'-'*79+ bcolors.ENDC)
    print(bcolors.FAIL + '-'*33 + 'OBJETO: %s' %halpha['num_gal'][i_gal] + '-'*33 + bcolors.ENDC)
    print(bcolors.FAIL +'-'*79+ bcolors.ENDC)
    plt.close()
    image_ha = fits.open('Hamaps/%s_%s_Ha.fits' %(halpha['num_gal'][i_gal],halpha['type'][i_gal]))
    img = get_image(image_ha)

    #plotando a imagem fits
    plt.figure(1)
    plt.clf()
    cx = cubehelix.cmap(reverse=True, start=0., rot=-0.5)
    plt.axis([0,77,0,72])
    plt.xlabel('X',fontweight='bold')
    plt.ylabel('Y',fontweight='bold')
    imgplot = plt.imshow(100*np.log10(img/255), cmap=cx)
    titulo='Galaxy %s ' %halpha['num_gal'][i_gal]
    plt.title(titulo)
    #plt.colorbar()
    figura = 'figures/galaxy_%s' %age['num_gal'][i_gal]
    plt.savefig(figura)

    #obtendo os dados da imagem fits
    df_ha = pd.DataFrame()
    nrows, ncols = img.shape
    xx, yy = np.meshgrid( *np.ogrid[:ncols, :nrows] )
    table = np.column_stack(( xx.flatten(), yy.flatten(), img.flatten() ))
    temp = pd.DataFrame(table, columns=['x','y','halpha'])
    df_ha = pd.concat([df_ha,temp], axis=1)

    #selecionando apenas os dados de idade > 0 e mass > 0
    df = df_ha[(df_ha.halpha > 0.0)]






fim = time.time()
time_proc = fim - ini
print('')
#print(bcolors.FAIL +'-'*79+ bcolors.ENDC)
print(bcolors.OKBLUE + 'tempo de processamento: %fs' %time_proc + bcolors.ENDC)
