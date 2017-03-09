  # -*- coding: utf-8 -*-

'''
Programa para trabalhar os dados do CALIFA
Uma nova abordagem, sem separacao de populacoes estelares
Retomando minha pesquisa... Que o Universo me ajude!

Versão 2.0
07-dezembro-2016
------------------

Versão 2.1
22-fevereiro-2017
Adição dos perfis radiais circulares


------------------
Versão 2.2
24-fevereiro-2017

-Adição de uma função para o cálculo da excentricidade da elipse e
ângulo de inclinação, para cálculo dos perfis radiais elípticos

-Normalização dos raios médios
-Adição dos std nas medidas

-------------------
Versão 2.2.1
06-março-2017

-Cálculo de momentos, parâmetros da elipse e centróides através de módulos a parte
-Cálculo dos perfis radiais elipticos


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
import momentos as mom
from matplotlib.patches import Ellipse
import matplotlib as mpl

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


def get_image(f_sdss):
    '''definindo a funcao que ira ler as imagens fits'''
    img = f_sdss[0].data
    return img

def C(df):
    '''funcao que calcula a Concentracao de uma populacao, usando a definicao
    de Conselice(2014) http://iopscience.iop.org/article/10.1086/375001/pdf
    '''
    a=1
    radius=df.sort_values('raio')
    r20=radius.iat[int(0.2*len(df)),-1]
    r80=radius.iat[int(0.8*len(df)),-1]
    Conc = 5*np.log((r80/r20))
    return Conc

def Z(df0,gal,Conc,ordem):
    '''definindo uma funcao para ordenar a propridade de interesse
    dividindo-o em bins de igual tamanho e calculando alguns parametros'''
    df_Z = pd.DataFrame()
    propr = []
    err_prop = []
    raio = []
    err_raio = []
    halpha = []
    err_halpha = []
    dens = []
    err_dens = []
    idade = []
    err_age = []
    semia = []
    err_semia = []
    conc = []

    df = df0.sort_values(by=ordem)
    df = df.reset_index()
    del df['index']

    cx, cy = mom.centro_mass(df)
    delta = len(df)/50 #Quantidade de bins
    j=0
    for i in range(0,(len(df)), delta):
        df1 = df.ix[i:i+delta,:]
        propr.append(df1[ordem].mean())
        err_prop.append(df1[ordem].std())
        raio.append(df1['raio'].mean())
        err_raio.append(df1['raio'].std())
        halpha.append(df1['halpha'].mean())
        err_halpha.append(df1['halpha'].std())
        dens.append(df1['mass'].mean())
        err_dens.append(df1['mass'].std())
        idade.append(df1['age'].mean())
        err_age.append(df1['age'].std())
        semia.append(df1['a'].mean())
        err_semia.append(df1['a'].std())
        conc.append(C(df1))
        j=j+1
    df_Z[ordem] = propr
    df_Z['erro'] = err_prop
    df_Z['raio_m'] = raio
    df_Z['err_raio'] = err_raio
    df_Z['age_m'] = idade
    df_Z['err_age'] = err_age
    df_Z['mass_m'] = dens
    df_Z['err_mass'] = err_dens
    df_Z['halpha_m'] = halpha
    df_Z['err_halpha'] = err_halpha
    df_Z['a_m'] = semia
    df_Z['err_a'] = err_semia
    df_Z[Conc] = conc
    return df_Z

def obtendo_dados(img,tipo):
    '''função para leitura do arquivo fits, criando um dataframe com os dados'''
    df = pd.DataFrame()
    nrows, ncols = img.shape
    xx, yy = np.meshgrid( *np.ogrid[:ncols, :nrows] )
    table = np.column_stack(( xx.flatten(), yy.flatten(), img.flatten() ))
    temp = pd.DataFrame(table, columns=['x','y',tipo])
    df = pd.concat([df,temp], axis=1)
    return(df)

def plots(df,param1,param2,param3):
    '''Função para plotar os gráficos'''
    plt.figure()
    incr = param3*(df.ix[:,0].mean())
    plt.xlim([(df.ix[:,0].min()-(incr)),(df.ix[:,0].max()+(incr))])
    plt.scatter(df.ix[:,0], df.ix[:,12])
    plt.title(gal)
    plt.ylabel('Concentraction')
    plt.xlabel(param2)
    plt.savefig('figures/concentracao/gal%s_concentration_%s' %(param1,param2))
    plt.close()

    plt.figure()
    plt.title('Distribuicao C(%s)- %s' %(param2,param1))
    df.ix[:,0].hist(bins=100)
    plt.savefig('figures/concentracao/gal%s_hist_%s' %(param1,param2))
    plt.close()

data_dir = '/home/pnovais/Dropbox/DOUTORADO/renew'
age = pd.read_csv('Paty_at_flux__yx/age.csv')
mass = pd.read_csv('PatImages/mass.csv')
halpha = pd.read_csv('Hamaps/halpha.csv')
#halpha = pd.read_csv('Hamaps/teste.csv')

hu1 = []
hu2 = []
hu3 = []
hu4 = []
hu5 = []
hu6 = []
hu7 = []
hugal = []
hutype = []

df_hu = pd.DataFrame()

for i_gal in range(len(halpha)):
#for i_gal in range(0,2):
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
    figura = 'figures/imagens_Ha/galaxy_%s' %halpha['num_gal'][i_gal]
    plt.savefig(figura)

    #obtendo os dados de Halpha da imagem fits
    df_ha = obtendo_dados(img,'halpha')

    #obtendo os dados de densidade de massa da imagem fits
    image_mass = fits.open('PatImages/PatImagesMcorSD__yx_%s.fits' %halpha['num_gal'][i_gal])
    img = get_image(image_mass)
    df_mass = obtendo_dados(img, 'mass')

    #obtendo os dados de idade da imagem fits
    image_age = fits.open('Paty_at_flux__yx/at_flux__yx_%s.fits' %halpha['num_gal'][i_gal])
    img = get_image(image_age)
    df_age = obtendo_dados(img, 'age')

    #selecionando apenas os dados de idade > 0 e mass > 0
    df0 = pd.merge(df_age,df_mass)
    df1 = pd.merge(df0,df_ha, how='inner')
    df = df1[(df1.age > 0.0) & (df1.mass > 0.0) & (df1.halpha > 0.0)]

    cx, cy = mom.centro_mass(df)
    tetha, exc, a, b = mom.param_elipse(df)
    df['raio'] = np.sqrt((df['x'] - cx)**2 + (df['y'] - cy)**2)
    acres = math.radians(180)
    d = ((df['x'] - cx)*np.cos(tetha) + (df['y'] - cy)*np.sin(-tetha+acres))**2
    e = ((df['x'] - cx)*np.sin(tetha) + (df['y'] - cy)*np.cos(-tetha+acres))**2
    df['a'] = np.sqrt(d + e/((1-exc)**2))

    gal = halpha['num_gal'][i_gal]
    tipo = halpha['type'][i_gal]

    age_test = Z(df,gal,'conc_age','age')
    mass_test = Z(df,gal,'conc_mass','mass')
    ha_test = Z(df,gal,'conc_ha','halpha')
    raio_test = Z(df,gal,'conc_raio', 'raio')
    a_test = Z(df,gal, 'conc_a', 'a')

    plots(age_test,gal,'Age',0)
    plots(mass_test,gal,'Mass_density',1)
    plots(ha_test,gal,'Halpha',1)

#perfis circulares
    plt.figure(1)
    plt.title(gal)
    ax1 = plt.subplot(311)
    plt.title('%s - %s' %(gal, tipo))
    ax1.errorbar(raio_test.raio_m, raio_test.age_m, yerr=raio_test.err_age, fmt='o')
    plt.plot(raio_test.raio_m, raio_test.age_m, color='#7e2601',linewidth=1)
    plt.ylabel('Mean Age')
    plt.setp(ax1.get_xticklabels(), visible=False)

    ax2 = plt.subplot(312, sharex=ax1)
    plt.ylim([(raio_test.halpha_m.min()-(raio_test.err_halpha.max() + 1e-17)),
             (raio_test.halpha_m.max()+(raio_test.err_halpha.max() + 1e-17))])
    ax2.errorbar(raio_test.raio_m, raio_test.halpha_m, yerr=raio_test.err_halpha, fmt='o')
    plt.plot(raio_test.raio_m, raio_test.halpha_m, color='#7e2601',linewidth=1)
    plt.ylabel('Mean Halpha')
    plt.setp(ax2.get_xticklabels(), visible=False)

    ax3 = plt.subplot(313, sharex=ax2)
    ax3.errorbar(raio_test.raio_m, raio_test.mass_m, yerr=raio_test.err_mass, fmt='.')
    plt.plot(raio_test.raio_m, raio_test.mass_m, color='#7e2601',linewidth=1)
    plt.ylabel('Mean mass density')
    plt.xlabel('Raio')
    plt.savefig('figures/perfis_circular/gal%s_perfis_circ' %(gal))
    plt.close(1)


    plt.figure()
    plt.scatter(raio_test.raio_m, raio_test.conc_raio)
    plt.plot(raio_test.raio_m, raio_test.conc_raio, color='#7e2601',linewidth=1)
    plt.title(gal)
    plt.ylabel('Concentraction')
    plt.xlabel('Raio')
    plt.savefig('figures/perfis_circular/gal%s_perfil_concentracao_circ' %(gal))
    plt.close()

#perfis elipticos
    plt.figure(1)
    plt.title(gal)
    ax1 = plt.subplot(311)
    plt.title('%s - %s' %(gal, tipo))
    ax1.errorbar(a_test.a_m, a_test.age_m, yerr=a_test.err_age, fmt='o')
    plt.scatter(a_test.a_m, a_test.age_m)
    plt.plot(a_test.a_m, a_test.age_m, color='#7e2601',linewidth=1)
    plt.ylabel('Mean Age')
    plt.setp(ax1.get_xticklabels(), visible=False)

    ax2 = plt.subplot(312, sharex=ax1)
    plt.ylim([(a_test.halpha_m.min()-(a_test.err_halpha.max() + 1e-17)),
             (a_test.halpha_m.max()+(a_test.err_halpha.max() + 1e-17))])
    ax2.errorbar(a_test.a_m, a_test.halpha_m, yerr=a_test.err_halpha, fmt='o')
    plt.plot(a_test.a_m, a_test.halpha_m, color='#7e2601',linewidth=1)
    plt.ylabel('Mean Halpha')
    plt.setp(ax2.get_xticklabels(), visible=False)

    ax3 = plt.subplot(313, sharex=ax2)
    ax3.errorbar(a_test.a_m, a_test.mass_m, yerr=a_test.err_mass, fmt='.')
    plt.plot(a_test.a_m, a_test.mass_m, color='#7e2601',linewidth=1)
    plt.ylabel('Mean mass density')
    plt.xlabel('Semi-eixo a')
    plt.savefig('figures/perfis_eliptico/gal%s_perfis_elip' %(gal))
    plt.close(1)


    plt.figure()
    plt.scatter(a_test.a_m, a_test.conc_a)
    plt.plot(a_test.a_m, a_test.conc_a, color='#7e2601',linewidth=1)
    plt.title(gal)
    plt.ylabel('Concentraction')
    plt.xlabel('Semi-eixo a')
    plt.savefig('figures/perfis_eliptico/gal%s_perfil_concentracao_elip' %(gal))
    plt.close()

    mean = [cx,cy]
    width = 2*a
    height = 2*b
    angle = math.degrees(tetha)
    ell = mpl.patches.Ellipse(xy=mean, width=width, height=height, angle = 180+angle, alpha=0.2, color='black')
    fig, ax = plt.subplots()
    ax.add_patch(ell)
    ax.autoscale()
    df2 = df.ix[(df.a > a/3) & (df.a < (a/3 + 2))]
    df3 = df.ix[(df.a > a/2) & (df.a < (a/2 + 2))]
    df4 = df.ix[(df.a > a) & (df.a < (a + 2))]
    plt.scatter(df.x,df.y, c='red', s=10, alpha=0.7)
    plt.scatter(df2.x,df2.y, c='blue')
    plt.scatter(df3.x,df3.y, c='purple')
    plt.scatter(df4.x, df4.y, c='green')
    plt.savefig('figures/ajuste_elipse/gal%s_elipses' %(gal))
    plt.close()
    print('excentricidade = %f' %exc)
    print('inclinacao = %f' %(math.degrees(tetha)))
    print('#%d' %i_gal)

    hu = mom.hu_moments(df)
    hu1.append(hu[0])
    hu2.append(hu[1])
    hu3.append(hu[2])
    hu4.append(hu[3])
    hu5.append(hu[4])
    hu6.append(hu[5])
    hu7.append(hu[6])
    hugal.append(gal)
    hutype.append(tipo)


df_hu['gal'] = hugal
df_hu['tipo'] = hutype
df_hu['hu1'] = hu1
df_hu['hu2'] = hu2
df_hu['hu3'] = hu3
df_hu['hu4'] = hu4
df_hu['hu5'] = hu5
df_hu['hu6'] = hu6
df_hu['hu7'] = hu7
#df_hu['hu1','hu2','hu3','hu4','hu5','hu6','hu7'] = hu1

df_hu.to_csv('hu_moments_gal.csv', index=False)

fim = time.time()
time_proc = fim - ini
print('')
#print(bcolors.FAIL +'-'*79+ bcolors.ENDC)
print(bcolors.OKBLUE + 'tempo de processamento: %fs' %time_proc + bcolors.ENDC)
