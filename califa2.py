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



fim = time.time()
time_proc = fim - ini
print('')
#print(bcolors.FAIL +'-'*79+ bcolors.ENDC)
print(bcolors.OKBLUE + 'tempo de processamento: %fs' %time_proc + bcolors.ENDC)
