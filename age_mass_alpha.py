#code = utf-8
'''
Programa criado para gerar os dados, pixel a pixel, para as galaxias do CALIFA:
-Idade estelar ponderada pela luminosidade
-Densidade de massa
-Halpha

25/nov: adicionando os parametros globais
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
import hu
import plots

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


data_dir = '/home/pnovais/Dropbox/DOUTORADO/granada_2016'
age = pd.read_csv('Paty_at_flux__yx/age.csv')
mass = pd.read_csv('PatImages/mass.csv')
halpha = pd.read_csv('Hamaps/halpha.csv')

globais = pd.read_csv('data/califa_master_list_rgb_2012.csv')

#selecionando os parametros globais de interesse, fazendo um match entre as tabelas
#pg = parametros globais
pg = pd.DataFrame()
k_num = []
d_mpc = []
Mr = []
ur = []
veldisp = []
re = []
r90 = []
r20 = []

for i in range(len(age)):
    for j in range(len(globais)):
        if (globais['#CALIFA_ID'][j] == age['num_gal'][i]):
            k_num.append(globais['#CALIFA_ID'][j])
            d_mpc.append(globais['d_Mpc'][j])
            Mr.append(globais['Mr'][j])
            ur.append(globais['u-r'][j])
            veldisp.append(globais['velDisp'][j])
            re.append(globais['re'][j])
            r90.append(globais['r90'][j])
            r20.append(globais['r20'][j])

pg['num_gal'] = k_num
pg['d_mpc'] = d_mpc
pg['Mr'] = Mr
pg['ur'] = ur
pg['veldisp'] = veldisp
pg['re'] = re
pg['r90'] = r90
pg['r20'] = r20


for i_gal in range(len(age)):
#for i_gal in range(0,3):
    print(bcolors.FAIL +'-'*79+ bcolors.ENDC)
    print(bcolors.FAIL + '-'*33 + 'OBJETO: %s' %age['num_gal'][i_gal] + '-'*33 + bcolors.ENDC)
    print(bcolors.FAIL +'-'*79+ bcolors.ENDC)
    plt.close()
    image_age = fits.open('Paty_at_flux__yx/at_flux__yx_%s.fits' %age['num_gal'][i_gal])
    #image_age = fits.open('at_flux__yx_K0127_original.fits')
    img = get_image(image_age)

    #plotando a imagem fits
    plt.figure(1)
    plt.clf()
    cx = cubehelix.cmap(reverse=True, start=0., rot=-0.5)
    plt.axis([0,77,0,72])
    plt.xlabel('X',fontweight='bold')
    plt.ylabel('Y',fontweight='bold')
    imgplot = plt.imshow(100*np.log10(img/255), cmap=cx)
    titulo='Galaxy %s ' %age['num_gal'][i_gal]
    plt.title(titulo)
    #plt.colorbar()
    figura = 'figures2/galaxy_%s' %age['num_gal'][i_gal]
    plt.savefig(figura)

    #obtendo os dados da imagem fits
    df_age = pd.DataFrame()
    nrows, ncols = img.shape
    xx, yy = np.meshgrid( *np.ogrid[:ncols, :nrows] )
    table = np.column_stack(( xx.flatten(), yy.flatten(), img.flatten() ))
    temp = pd.DataFrame(table, columns=['x','y','age'])
    df_age = pd.concat([df_age,temp], axis=1)

    image_mass = fits.open('PatImages/PatImagesMcorSD__yx_%s.fits' %age['num_gal'][i_gal])
    #image_age = fits.open('at_flux__yx_K0127_original.fits')
    img = get_image(image_mass)

    #obtendo os dados da imagem fits
    df_mass = pd.DataFrame()
    nrows, ncols = img.shape
    xx, yy = np.meshgrid( *np.ogrid[:ncols, :nrows] )
    table = np.column_stack(( xx.flatten(), yy.flatten(), img.flatten() ))
    temp = pd.DataFrame(table, columns=['x','y','mass'])
    df_mass = pd.concat([df_mass,temp], axis=1)

    df0 = pd.merge(df_age,df_mass)

    #selecionando apenas os dados de idade > 0 e mass > 0
    df = df0[(df0.age > 0.0) & (df0.mass > 0.0)]


    #ordenando os dados pela idade
    df2 = df.sort_values(by='age')
    df2 = df2.reset_index()
    del df2['index']

    #dividindo as populacoes
    compr = len(df2)

    pop1 = df2.ix[:(compr/4),:]
    pop2 = df2.ix[(compr/4)+1:(compr/2),:]
    pop3 = df2.ix[(compr/2)+1:(3*(compr/4)),:]
    pop4 = df2.ix[(3*compr/4)+1:compr,:]

    #plotando as populacoes
    f, ((ax1,ax2), (ax3,ax4)) = plt.subplots(2,2, sharex='col', sharey='row')
    plt.axis([0,77,0,72])
    ax1.scatter(pop1['x'],pop1['y'], color="#2b83ba")
    ax2.scatter(pop2['x'],pop2['y'], color="#abdda4")
    ax3.scatter(pop3['x'],pop3['y'], color="#fdae61")
    ax4.scatter(pop4['x'],pop4['y'], color="#d7191c")
    plt.savefig('figures2/Distribution_4panel_gal_%s.png' %(age['num_gal'][i_gal]))

    plt.figure()
    plt.axis([0,77,0,72])
    plt.xlabel('X', fontweight='bold')
    plt.ylabel('Y', fontweight='bold')
    plt.title(titulo)
    plt.scatter(pop1['x'],pop1['y'], color="#2b83ba")
    plt.scatter(pop2['x'],pop2['y'], color="#abdda4")
    plt.scatter(pop3['x'],pop3['y'], color="#fdae61")
    plt.scatter(pop4['x'],pop4['y'], color="#d7191c")
    plt.savefig('figures2/Distribution_all_gal_%s.png' %(age['num_gal'][i_gal]))
    #plt.show()
    '''
    ================================================================================
    Calculando os momentos invariantes de Hu
    ================================================================================

    !======================================================
    !================CENTROIDES DA IMAGEM==================
    !======================================================
    !xc = M10/M00
    !yc = M01/M00
    !
    !onde xc e yc sao os centroides da imagem, M10, M01 e
    !M00 os momentos nao centrais, onde
    !
    !Mpq=Somatorio(x^p.y^q)
    !------------------------------------------------------
    '''

    m10=df2['x'].sum()
    m01=df2['y'].sum()
    cx = int(m10/len(df2))
    cy = int(m01/len(df2))
    re = np.sqrt(len(df2)/3.14)
    tm_total = df2['age'].mean()
    tm_total_std = df2['age'].std()
    mass_t = df2.mass.sum()
    mass_m = df2.mass.mean()
    mass_m_std = df2.mass.std()

    print(bcolors.PATY + 'Properties' + bcolors.ENDC)
    print('Idade media galaxia: %5.3f+-%5.3f Gyr' %(tm_total,tm_total_std))
    print('Densidade de massa total: %5.3f Msun/pc^2' %mass_t)
    print('Densidade de massa media: %5.3f+-%5.3f Msun/pc^2' %(mass_m,mass_m_std))
    print('Centroides (Cx,Cy) da imagem: (%d,%d)' %(cx,cy))
    print('Raio equivalente (m00/pi): %5.3f'%re)

    f = open('data/parametros_hu_%s.txt' %(age['num_gal'][i_gal]), 'w')
    f.write('obj  #Populacao Rm/re std tm tm_std tp tp_std M_t M_p I1  I2  I3  I4  I5  I6  I7  a   b   f=a+b/2 tetha   Exc     flong   Sim Conc\n')
    f.close()
    arquive = 'data/parametros_hu_%s.txt' %(age['num_gal'][i_gal])
    obj = str(age['num_gal'][i_gal])

    hu.Humoments(obj,arquive,pop1,re,cx,cy,tm_total,tm_total_std,mass_t,p=1)
    hu.Humoments(obj,arquive,pop2,re,cx,cy,tm_total,tm_total_std,mass_t,p=2)
    hu.Humoments(obj,arquive,pop3,re,cx,cy,tm_total,tm_total_std,mass_t,p=3)
    hu.Humoments(obj,arquive,pop4,re,cx,cy,tm_total,tm_total_std,mass_t,p=4)
    parc = time.time()
    time_parc = parc - ini
    print('tempo parcial: %fs (%d de %d)' %(time_parc,i_gal,len(age)))

    df2.to_csv('data/age_massdensity_%s.csv' %age['num_gal'][i_gal], index=False)
    print(' ')
#    print(len(df2))

plt.close()
early = pd.read_csv('data/group1/califa_group1.csv' )
late = pd.read_csv('data/group2/califa_group2.csv' )
irregular = pd.read_csv('data/group3/califa_group3.csv')

df_e = plots.juncao(early,'group1')
df_l = plots.juncao(late,'group2')
df_i = plots.juncao(irregular,'group3')

plt.close()
#plots.compare(df_e,df_l,df_i)


fim = time.time()
time_proc = fim - ini
print('')
#print(bcolors.FAIL +'-'*79+ bcolors.ENDC)
print(bcolors.OKBLUE + 'tempo de processamento: %fs' %time_proc + bcolors.ENDC)
