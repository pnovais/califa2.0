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


#definindo a funcao que ira ler as imagens fits
def get_image(f_sdss):
    img = f_sdss[0].data
#    sky = f_sdss[2].data
    return img

#funcao que calcula a Concentracao de uma populacao, usando a definicao
#de Conselice(2014) http://iopscience.iop.org/article/10.1086/375001/pdf
def C(df,cx,cy):
    df['raio'] = np.sqrt((df['x'] - cx)**2 + (df['y'] - cy)**2)
    a=1
    radius=df.sort_values('raio')
    r20=radius.iat[int(0.2*len(df)),-1]
    r80=radius.iat[int(0.8*len(df)),-1]
    Conc = 5*np.log((r80/r20))
    return Conc

#definindo uma funcao para ordenar a propridade de interesse
#dividi-lo em bins de igual tamanho e calcular alguns parametros
def Z(df0,gal,Conc,ordem):
    df_Z = pd.DataFrame()
    grades = []
    conc = []

    df = df0.sort_values(by=ordem)
    df = df.reset_index()
    del df['index']

    m10=df['x'].sum() #Calculando o momento m10
    m01=df['y'].sum() #Calculando o momento m01
    cx = int(m10/len(df)) #Calculando os centroides da imagem
    cy = int(m01/len(df))
    delta = len(df)/100 #Quantidade de bins
    j=0
    for i in range(0,(len(df)), delta):
        df1 = df.ix[i:i+delta,:]
        grades.append(df1[ordem].mean())
        conc.append(C(df1,cx,cy))
        j=j+1
    df_Z[ordem] = grades
    df_Z[Conc] = conc
    print(j,cx)
    print(len(df_Z))
    print(df_Z.head())
    return df_Z


#data_dir = '/home/pnovais/Dropbox/DOUTORADO/renew'
age = pd.read_csv('Paty_at_flux__yx/age.csv')
mass = pd.read_csv('PatImages/mass.csv')
halpha = pd.read_csv('Hamaps/halpha.csv')



#for i_gal in range(len(halpha)):
for i_gal in range(0,4):
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
    titulo='Halpha Maps - Galaxy %s ' %halpha['num_gal'][i_gal]
    plt.title(titulo)
    #plt.colorbar()
    figura = 'figures/galaxy_%s' %age['num_gal'][i_gal]
    plt.savefig(figura)

    #obtendo os dados de Halpha da imagem fits
    df_ha = pd.DataFrame()
    nrows, ncols = img.shape
    xx, yy = np.meshgrid( *np.ogrid[:ncols, :nrows] )
    table = np.column_stack(( xx.flatten(), yy.flatten(), img.flatten() ))
    temp = pd.DataFrame(table, columns=['x','y','halpha'])
    df_ha = pd.concat([df_ha,temp], axis=1)

    #obtendo os dados de densidade de massa da imagem fits
    image_mass = fits.open('PatImages/PatImagesMcorSD__yx_%s.fits' %halpha['num_gal'][i_gal])
    img = get_image(image_mass)

    df_mass = pd.DataFrame()
    nrows, ncols = img.shape
    xx, yy = np.meshgrid( *np.ogrid[:ncols, :nrows] )
    table = np.column_stack(( xx.flatten(), yy.flatten(), img.flatten() ))
    temp = pd.DataFrame(table, columns=['x','y','mass'])
    df_mass = pd.concat([df_mass,temp], axis=1)

    #obtendo os dados de idade da imagem fits
    image_age = fits.open('Paty_at_flux__yx/at_flux__yx_%s.fits' %halpha['num_gal'][i_gal])
    img = get_image(image_age)

    df_age = pd.DataFrame()
    nrows, ncols = img.shape
    xx, yy = np.meshgrid( *np.ogrid[:ncols, :nrows] )
    table = np.column_stack(( xx.flatten(), yy.flatten(), img.flatten() ))
    temp = pd.DataFrame(table, columns=['x','y','age'])
    df_age = pd.concat([df_age,temp], axis=1)

    #selecionando apenas os dados de idade > 0 e mass > 0
    df0 = pd.merge(df_age,df_mass)
    df1 = pd.merge(df0,df_ha, how='inner')
    df = df1[(df1.age > 0.0) & (df1.mass > 0.0) & (df1.halpha > 0.0)]

    gal = halpha['num_gal'][i_gal]

    age_test = Z(df,gal,'conc_age','age')
    mass_test = Z(df,gal,'conc_mass','mass')
    ha_test = Z(df,gal,'conc_ha','halpha')

    plt.figure()
    plt.scatter(age_test.age, age_test.conc_age)
    plt.title(gal)
    plt.ylabel('Concentraction')
    plt.xlabel('Age')
    plt.savefig('figures/concentracao/gal%s_concentration_age' %(gal))
    plt.close()

    plt.figure()
    plt.title('Distribuicao C(age)- %s' %gal)
    age_test.age.hist(bins=100)
    plt.savefig('figures/concentracao/gal%s_hist_halpha' %(gal))
    plt.close()

    plt.figure()
    plt.scatter(mass_test.mass, mass_test.conc_mass)
    plt.title(gal)
    plt.ylabel('Concentraction')
    plt.xlabel('Mass density')
    plt.savefig('figures/concentracao/gal%s_concentration_mass' %(gal))
    plt.close()

    plt.figure()
    mass_test.mass.hist(bins=100)
    plt.title('Distribuicao C(mass) - %s' %gal)
    plt.savefig('figures/concentracao/gal%s_hist_halpha' %(gal))
    plt.close()

    plt.figure()
    plt.xlim([-5e-17,4e-16])
    plt.scatter(ha_test.halpha, ha_test.conc_ha)
    plt.title(gal)
    plt.ylabel('Concentraction')
    plt.xlabel('Halpha')
    plt.savefig('figures/concentracao/gal%s_concentration_halpha' %(gal))
    plt.close()

    plt.figure()
    ha_test.halpha.hist(bins=100)
    plt.title('Distribuicao C(halpha) - %s' %gal)
    plt.savefig('figures/concentracao/gal%s_hist_halpha' %(gal))
    plt.close()


fim = time.time()
time_proc = fim - ini
print('')
#print(bcolors.FAIL +'-'*79+ bcolors.ENDC)
print(bcolors.OKBLUE + 'tempo de processamento: %fs' %time_proc + bcolors.ENDC)
