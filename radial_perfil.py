 # -*- coding: utf-8 -*-

'''
Calculo dos perfis radiais
(22/02/2017)
- perfis em elipses de semi-eixo maior r: Z(r)
+ temos a elipticidade e e o semi-eixo maior da galaxia: eps, a
+ vamos considerar n bins: delta_r = a/n
+ considerar o valor medio e o erro da media de Z dentro de anéis elípticos de
semi-eixo maior (i-1)*delta_r e i*delta_r para i=1,...n
+ para isso tem que saber que galaxia cai dentro de cada anel
'''

import pandas as pd
import numpy as np
import datetime
import time
from sys import exit
from matplotlib import colors, pyplot as plt
from functools import reduce
import matplotlib.cm as cm
from astropy.io import ascii, fits
from astropy.wcs import wcs
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from scipy.interpolate import interp2d
import cubehelix
import matplotlib.mlab as mlab
#import scipy, pylab
#import math

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


data_dir = '/home/pnovais/Dropbox/DOUTORADO/renew'
age = pd.read_csv('Paty_at_flux__yx/age.csv')
mass = pd.read_csv('PatImages/mass.csv')
halpha = pd.read_csv('Hamaps/halpha.csv')









fim = time.time()
time_proc = fim - ini
print('')
#print(bcolors.FAIL +'-'*79+ bcolors.ENDC)
print(bcolors.OKBLUE + 'tempo de processamento: %fs' %time_proc + bcolors.ENDC)
