# RETOMANDO MINHAS ANÁLISES 
CALIFA 2.0 Reiniciando os projetos

Esta wiki servirá para documentar os passos realizados no estudo de populações estelares espacialmente resolvidas, em galáxias do projeto CALIFA. 

_**Author:**_ Patricia Novais.

***

Acesse a Wiki [aqui.](https://github.com/pnovais/califa2.0/wiki)

Acesse o github [aqui.](https://github.com/pnovais/califa2.0)

***

## Amostras

As imagens, em cores falsas, podem ser visualizadas [aqui.](https://www.dropbox.com/sh/a2n1uwyhihrh6b1/AACTP_JX9nqvLgMg-vjeRx1ma?dl=0)

### Principal
276 objetos, com dados espacialmente resolvidos de:

   * Idade ponderada pela luminosidade
   * Emissão em Halpha
   * Densidade de massa

### Controle (apenas para teste de algoritmo e primeiros resultados)
8 objetos, de 4 tipos morfológicos:

   * 2 elípticas, E1 e E7
   * 2 lenticulares, S0
   * 2 espirais, Sb
   * 2 tardias, Sd

**Galáxias Elípticas:**

* K0035 - [NGC0364](http://www.caha.es/CALIFA/public_html/?q=content/califa-explorer-v01&califaid=35)
* K0602 - [NGC4956](http://www.caha.es/CALIFA/public_html/?q=content/califa-explorer-v01&califaid=602)

**Galáxias S0:**

* K0047 - [NGC0517](http://www.caha.es/CALIFA/public_html/?q=content/califa-explorer-v01&califaid=47)
* K0607 - [UGC08264](http://www.caha.es/CALIFA/public_html/?q=content/califa-explorer-v01&califaid=607)

**Galáxias Espirais:**

* K0010 - [NGC0036](http://www.caha.es/CALIFA/public_html/?q=content/califa-explorer-v01&califaid=10)
* K0023 - [NGC0171](http://www.caha.es/CALIFA/public_html/?q=content/califa-explorer-v01&califaid=23)

**Galáxias Irregulares:**

* K0014 - [UGC00312](http://www.caha.es/CALIFA/public_html/?q=content/califa-explorer-v01&califaid=14)
* K0027 - [NGC0216](http://www.caha.es/CALIFA/public_html/?q=content/califa-explorer-v01&califaid=27)

***

## P-a-P
Para cada propriedade Z (idade, Halpha ou densidade de massa), calcula-se a concentração C(Z), da seguinte forma:

* Para cada propr. Z, ordenar e separar em bins com o mesmo número de pontos
* bins=100
* Para cada bin, calculamos a concentração C(Z)
    * C(Z) = 5 log(r80/r20) [See Conselice(2003,2014)](http://iopscience.iop.org/article/10.1086/375001/pdf)
* Plots de C(Z)


### Perfis

Para maiores detalhes, veja [Perfis](https://github.com/pnovais/califa2.0/wiki/Simula%C3%A7%C3%B5es)

1a fase: 
* galaxias circulares
* pixelização (x,y,r)
* Z = Z(r) + sigma
* calculo dos parametros


2a fase - perfil elíptico: 
* galaxias elípticas
* pixelização (x,y,a), com *a* sendo o semi-eixo maior da elipse
* Z = Z(r) + sigma
* Perfil dos parâmetros, em função do semi-eixo maior a.
***

### Primeiros testes com a amostra de controle
Os gráficos de C(Z) e das distribuições das propriedades Z's, podem ser vistas na aba [Primeiros gráficos](https://github.com/pnovais/califa2.0/wiki/Primeiros-gr%C3%A1ficos)

**Idade**

Com excessão das galáxias tardias, todas as demais galáxias mostram uma tendência que quanto maior a idade do bin maior será a concentração.

**Densidade de massa**

Apesar de não ser muito claro, a densidade de massa tende a aumentar com a idade

**H-alpha**

As galáxias espirais parecem ter dois comportamentos, enquanto que as tardias aumenta Halpha com a idade.

***
### H-alpha - Análises
[H-alpha - Análises](https://github.com/pnovais/califa2.0/wiki/H-alpha-Analysis)

Focando na análises apenas da emissão em Halpha, iremos tentar encontrar padrões nos perfis radiais e nas concentrações C(Halpha)

As galáxias do tipo E e S0 podem ser separadas em 3 tipos de de perfil de Halpha.

*Perfis tipo A, B e D*
![perfilabd](https://github.com/pnovais/califa2.0/blob/master/abd.png)


*Perfis tipo E, F e G*
![perfilefg](https://github.com/pnovais/califa2.0/blob/master/efg.png)
