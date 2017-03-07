
# -*- coding: utf-8 -*-

'''
Módulo para cálculo dos momentos invariantes das imagens
Author: Patricia Novais
06-março-2017
São Paulo - SP
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

def centro_mass(df):
    #não centrais de 1 ordem
    m10=df['x'].sum() #Calculando o momento m10
    m01=df['y'].sum() #Calculando o momento m01
    cx = int(m10/len(df)) #Calculando os centroides da imagem
    cy = int(m01/len(df))
    return(cx,cy)

def m_naocentrais(df):
    #nao centrais de 2 ordem
    m11=(df['x']*df['y']).sum()
    m20=(df['x']*df['x']).sum()
    m02=(df['y']*df['y']).sum()
    return(m11, m20, m02)

def m_centrais(df):
    cx, cy = centro_mass(df)
    m11, m20, m02 = m_naocentrais(df)
    #centrais de 2 ordem
    mu_11=((df['x']-cx)*(df['y']-cy)).sum()
    mu_20=((df['x']-cx)**2).sum()
    mu_02=((df['y']-cy)**2).sum()
    #centrais de 3 ordem
    mu_12=((df['x']-cx)*((df['y']-cy)**2)).sum()
    mu_21=((df['y']-cx)*((df['x']-cx)**2)).sum()
    mu_30=((df['x']-cx)**3).sum()
    mu_03=((df['y']-cy)**3).sum()
    return(mu_11, mu_20, mu_02, mu_12, mu_21, mu_30, mu_03)

def m_invEscala(df):
    mu_11, mu_20, mu_02, mu_12, mu_21, mu_30, mu_03= m_centrais(df)
    n11=mu_11/(len(df)**2)
    n12=mu_12/(len(df)**2.5)
    n21=mu_21/(len(df)**2.5)
    n02=mu_02/(len(df)**2)
    n20=mu_20/(len(df)**2)
    n30=mu_30/(len(df)**2.5)
    n03=mu_03/(len(df)**2.5)
    return(n11, n21, n12, n20, n02, n30, n03)

def hu_moments(df):
    n11, n21, n12, n20, n02, n30, n03 = m_invEscala(df)
    I1 = n02 + n20
    I2 = ((n20-n02)**2) + 4*((n11)**2)
    I3 = (n30 - 3*n12)**2 + (3*n21 - n03)**2
    I4 = (n30 + 3*n12)**2 + (3*n21 + n03)**2
    I5 = (n30 - 3*n12)*(n30 + n12)*(((n30 + n12)**2) - 3*((n21 + n03)**2)) + (3*n21 - n03)*(n12 + n03)*(3*((n30 + n12)**2) - ((n21 + n03)**2))
    I6 = (n20 - n02)*((n30 + n12)**2 - (n21 + n03)**2) + 4*n11*(n30 + n12)*(n21 + n03)
    I7 = (3*n21 - n03)*(n30 + n12)*((n30 + n12)**2 - 3*(n21 + n03)**2) - (n30 - 3*n12)*(n21 + n03)*(3*(n30 + n12)**2 - (n21 + n03)**2)
    return(I1, I2, I3, I4, I5, I6, I7)

def param_elipse(df):
    mu_11, mu_20, mu_02, mu_12, mu_21, mu_30, mu_03 = m_centrais(df)
    #Parametros da Elipse
    dd = (mu_20 + mu_02)
    ee = (mu_20 - mu_02)*(mu_20 - mu_02) + 4*(mu_11)*(mu_11)
    a = np.sqrt((2*(dd + np.sqrt(ee)))/len(df))
    b = np.sqrt((2*(dd - np.sqrt(ee)))/len(df))
    #Orientacao da Elipse
    tetha = 0.5*np.arctan2((2*mu_11),(mu_20 - mu_02))
    #Excentricidade
    exc = 1 - (b/a)
    return(tetha,exc,a,b)

#df = pd.read_csv('unit_test.csv')

#y = centro_mass(df)


fim = time.time()
time_proc = fim - ini
print('')
print('tempo de processamento: %fs' %time_proc)
