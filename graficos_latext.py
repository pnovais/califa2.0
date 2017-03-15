import numpy as np
import pandas as pd


file=open('latex.txt', 'a')
dfi = pd.read_csv('imagens.txt')
dfc = pd.read_csv('concent.txt')
dfp = pd.read_csv('perfis.txt')

for i in range(len(dfi)):
    file.write('\\begin{figure}[!ht]\n')
    file.write('\\begin{center}\n')
    file.write('\\setcaptionmargin{1cm}\n')
    file.write('\\includegraphics[width=0.3 \columnwidth,angle=0]{fig/%s}\n' %dfi['#obj'][i])
    file.write('\\includegraphics[width=0.3 \columnwidth,angle=0]{fig/%s}\n' %dfc['#obj'][i])
    file.write('\\includegraphics[width=0.3 \columnwidth,angle=0]{fig/%s}\n' %dfp['#obj'][i])
    file.write('\\end{center}\n')
    file.write('\\end{figure}\n')
    file.write('\n')
    file.write('\n')

file.close()
