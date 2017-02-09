# RETOMANDO MINHAS ANÁLISES 
CALIFA 2.0 Reiniciando os projetos

Esta wiki servirá para documentar os passos realizados no estudo de populações estelares espacialmente resolvidas, em galáxias do projeto CALIFA. 

_**Author:**_ Patricia Novais.

***

Acesse a Wiki [aqui.](https://github.com/pnovais/califa2.0/wiki)

Acesse o github [aqui.](https://github.com/pnovais/califa2.0)

***

## Amostras

As imagens, em cores falsas, podem ser visualizadas [aqui](https://www.dropbox.com/sh/a2n1uwyhihrh6b1/AACTP_JX9nqvLgMg-vjeRx1ma?dl=0)

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

* K0035 [NGC0364]
* K0602 [NGC4956]

**Galáxias S0:**

* K0047 [NGC0517]
* K0607 [UGC08264]

**Galáxias Espirais:**

* K0010 [NGC0036]
* K0023 [NGC0171]

**Galáxias Irregulares:**

* K0014 [UGC00312]
* K0027 [NGC0216]

***

## P-a-P
Para cada propriedade Z (idade, Halpha ou densidade de massa), calcula-se a concentração C(Z), da seguinte forma:

* Para cada propr. Z, ordenar e separar em bins com o mesmo número de pontos
* bins=100
* Para cada bin, calculamos a concentração C(Z)
    * C(z) = 5 log(r80/r20) [See Conselice(2003,2014)](http://iopscience.iop.org/article/10.1086/375001/pdf)
* Plots de C(Z)

***

### Primeiros testes com a amostra de controle
Os gráficos de C(Z) e das distribuições das propriedades Z's, podem ser vistas na aba [Primeiros gráficos](https://github.com/pnovais/califa2.0/wiki/Primeiros-gr%C3%A1ficos)

**Idade**

Com excessão das galáxias tardias, todas as demais galáxias mostram uma tendência que quanto maior a idade do bin maior será a concentração.

**Densidade de massa**

Apesar de não ser muito claro, a densidade de massa tende a aumentar com a idade

**H-alpha**

As galáxias espirais parecem ter dois comportamentos, enquanto que as tardias aumenta Halpha com a idade.
