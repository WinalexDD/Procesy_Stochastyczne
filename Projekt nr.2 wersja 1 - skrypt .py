#!/usr/bin/env python
# coding: utf-8

# # Biblioteki

# In[1]:


from pandas import read_csv, DataFrame 
import os 
from collections import Counter, OrderedDict
import matplotlib.pyplot as plt
import numpy as np
import random
from math import sqrt
from sympy import *
from netgraph import Graph
import matplotlib
matplotlib.use('Agg')


# # Wczytanie danych

# In[2]:


dir=input("Prosze podać ścieżke z katalogiem healthy_decades: ")
os.chdir(str(dir))


# # Punkt A

# # Zamiana serii na łańcuch

# In[3]:


def zamiana_na_stany(series, k):
    K=series.values
    mi=np.min(K)
    stany=[]
    for i in range(len(K)):
        stany.append(int((K[i]-mi)/(8*k)))
    return stany


# In[4]:


def rozne_k():
    k_values=random.sample(range(2, 10), 2)
    k_values.insert(0, 1)
    k_values.sort()
    return k_values


# In[5]:


def zamiana_na_łańcuch(seria):
    k=rozne_k()
    lancuchy=[]
    for wartosci in k:
        lancuchy.append(zamiana_na_stany(seria, wartosci))
    return lancuchy, k


# # Macierz przejścia

# In[6]:


def macierz_przejscia(stany, ilosc_stanow): 
    M = [[0]*ilosc_stanow for _ in range(ilosc_stanow)]
    for (i,j) in zip(stany,stany[1:]):
        M[i][j] += 1
        
    for row in M:
        s = sum(row)
        if s > 0:
            row[:] = [f/s for f in row]
    return M


# # Wizualizacja

# In[7]:


def wizualizacja(macierz, nazwa):
    sources, targets = np.where(macierz)
    weights = macierz[sources, targets]
    weights=np.around(weights, decimals=2, out=None)
    edges = list(zip(sources, targets))
    edge_labels = dict(zip(edges, weights))
    
    if len(targets)>200:
        fig, ax = plt.subplots(figsize=(50,50))
        Graph(edges,node_labels=True,arrows=True, ax=ax, node_label_fontdict=dict(size=9), node_size=1, edge_width=0.1, 
              node_layout="dot")
        plt.savefig(nazwa + " - graf.png")
        plt.clf()
        plt.close()
        
    else:
        fig, ax = plt.subplots(figsize=(50,50))
        Graph(edges,node_labels=True, edge_labels=edge_labels, edge_label_position=0.6,edge_label_fontdict=dict(size=6), 
              arrows=True, ax=ax, node_label_fontdict=dict(size=9), node_size=1, edge_width=0.1, node_layout="dot")
        plt.savefig(nazwa + " - graf.png")
        plt.clf()
        plt.close()


# # Klasyfikacja stanów

# In[8]:


def klasyfikacja_stanow(macierz):
    powr=[]
    przej=[]
    S=[]
    macierz0=macierz
    macierz1=macierz
    suma=macierz
    for n in range(10001):
        macierz0=np.dot(macierz0,macierz1)
        suma=suma+macierz0
        if n==1000:
            suma1=suma
        if n==10000:
            suma2=suma
    kl=suma2-suma1
    for i in range(len(macierz)):
        if kl[i][i]==0:
            przej.append(i)
        else:
            powr.append(i)
        S.append(i)
    return powr, przej, S


# # Stan stacjonarny

# # Metoda zagadnienia własnego

# In[9]:


def stacjo_metoda1(macierz):
    
    macierz_trans=macierz.T
    wartw, wektrw = np.linalg.eig(macierz_trans)
    close_to_1_idx = np.isclose(wartw,1)
    target_eigenvect = wektrw[:,close_to_1_idx]
    
    if target_eigenvect.size==0:
        return "Brak rozkładu stacjonarnego"
    
    target_eigenvect = target_eigenvect[:,0]
    rozkład_stacjo = target_eigenvect / sum(target_eigenvect)
    rozkład_stacjo=rozkład_stacjo.real
    
    return rozkład_stacjo


# # Metoda graniczna

# In[10]:


def stacjo_metoda2(macierz):
    
    pi = np.full((1, len(macierz)), 1/len(macierz))
    i=0
    
    while True:
        new_pi = np.dot(pi, macierz)
        if np.allclose(pi, new_pi):
            break
        pi = new_pi   
        i=i+1
        if i==5000:
            return "Brak rozkładu stacjonarnego"
        
    if (pi==np.zeros(len(macierz))).all():
        return "Brak rozkładu stacjonarnego"
    return pi 


# # Metoda Monte Carlo

# In[11]:


def sym(macierz):
    for row in macierz:
        s = sum(row)
        if s == 0:
            row[:] = [1/len(row) for _ in row]
        if s>0 and s<1:
            return "Macierz nie jest stochastyczna"
    symulacja=[]
    k=np.random.choice(np.arange(0, len(macierz)), p=np.full((1, len(macierz)), 1/len(macierz))[0])
    for i in range(50000):
        symulacja.append(k)
        k=np.random.choice(np.arange(0, len(macierz)), p=macierz[k])
    return symulacja
def stacjo_metoda3(stany):
    if isinstance(stany, str):
        return "Macierz nie jest stochastyczna"
    pi=[]
    for n in range(max(stany)+1):
        z=0
        for i in range (len(stany)):
            if stany[i]==n:
                z+=1
        pi.append(z/len(stany))
    return pi


# # Odwracalność

# In[12]:


def odwracalnosc(macierz, stacjo):
    if isinstance(stacjo, str):
        return "Łańcuch jest nieodwracalny"
    for i in range(len(macierz)):
        for j in range(len(macierz)):
            x=stacjo[i]*macierz[i][j]
            y=stacjo[j]*macierz[j][i]
            if x!=y:
                return "Łańcuch jest nieodwracalny"
                break
    return "Łańcuch jest odwracalny"


# # Tabela

# In[13]:


def punktA(macierz, nazwa):
    
    wizualizacja(np.array(macierz), nazwa)
    
    stacjo=stacjo_metoda1(np.array(macierz))
    klasy_stanow=klasyfikacja_stanow(macierz)
    fig, ax = plt.subplots()
    df1=DataFrame(data={'Tabela': ["Lista stanów:", klasy_stanow[2], "Stany powracające:", klasy_stanow[0], 
                                             "Stany przechodnie:", klasy_stanow[1], 'Stan stacjonarny - metoda 1', 1,
                                             'Stan stacjonarny - metoda 2',1, 
                                              'Stan stacjonarny - metoda 3',1, 
                                            "Czy łańcuch jest odwracalny:", odwracalnosc(np.array(macierz), stacjo)]})
    tabelawykres=plt.table(cellText=df1.values, cellLoc='center', rowLabels=df1.index, colLabels=df1.columns, 
                           loc='upper center')
    ax.axis("off")
    tabelawykres.add_cell(8, 0, width=1, height=0.15, text=stacjo, loc='center')
    tabelawykres.add_cell(10, 0, width=1, height=0.15, text=stacjo_metoda2(macierz), loc='center')
    tabelawykres.add_cell(12, 0, width=1, height=0.15, text=np.array(stacjo_metoda3(sym(macierz))), loc='center')
    tabelawykres.auto_set_font_size(False)
    tabelawykres.set_fontsize(23)
    plt.gcf().set_size_inches(80, 60)
    plt.savefig(nazwa + ' - tabela.png')
    plt.clf()
    plt.close()


# # Punkt B

# In[14]:


def punktB(seria, nazwa):
    for i in [1,2,3,10]:
        s=seria.diff(periods=i).dropna()
        punktA(macierz_przejscia(zamiana_na_stany(s, 1), max(zamiana_na_stany(s, 1))+1),
               nazwa + "- RR_" + str(i))


# # Punkt C

# In[15]:


def punktC(seria, nazwa):
    stany=zamiana_na_stany(seria, 1)
    ilosc_stanow=max(stany)+1
    for i in [30,60,120,200]:   
        median=[]
        std=[]
        macierze=[]
        for n in range(int(len(seria)/i)):
            x=seria.values[n*i:n*i+i].tolist()
            median.append(np.median(x))
            std.append(np.std(x))
            x=stany[n*i:n*i+i]
            macierze.append(macierz_przejscia(x, ilosc_stanow))
            
        max_median_index=np.array(median).argmax()
        min_median_index=np.array(median).argmin()
        max_std_index=np.array(std).argmax()
        min_std_index=np.array(std).argmin()
        okna={"Największa mediana": max_median_index, "Najmniejsza mediana": min_median_index, 
              "Największe odchylenie standardowe": max_std_index, "Najmniejsze odchylenie standardowe": min_std_index}
        
        for name, index in okna.items():
            window=stany[index*i:index*i+i]
            macierz=macierz_przejscia(window, max(window)+1)
            punktA(macierz, nazwa + " - okno rozm." + str(i) + " - " + name)
            
        usredniona_macierz=np.mean(np.array(macierze), axis=0 )
        blad=np.std(np.array(macierze))/sqrt(len(np.array(macierze)))
        punktA(usredniona_macierz, nazwa + " - okno rozm." + str(i) +" - Uśredniona macierz")


# # Punkt D

# In[16]:


def punktD(seria, nazwa):
    for i in [1,2,3,10]:
        s=seria.diff(periods=i).dropna().values.tolist()
        s2=[]
        s3=[]
        for k in range(len(s)):
            if s[k][0]>0:
                if abs(s[k][0])>0 and abs(s[k][0])<40:
                    s[k]="d"
                else:
                    s[k]="D"
            elif s[k][0]==0:
                    s[k]="Z"
            else:
                if abs(s[k][0])>0 and abs(s[k][0])<40:
                    s[k]="a"
                else:
                    s[k]="A"
            if k%2==1:
                s2.append(s[k-1]+s[k])
            if k%3==2:   
                s3.append(s[k-2]+s[k-1]+s[k])
        
        X=OrderedDict(Counter(s).most_common())
        Y=OrderedDict(Counter(s2).most_common())
        Z=OrderedDict(Counter(s3).most_common())
        fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, ncols=1, figsize=(20,15))
        ax0.bar(list(X.keys()), X.values())
        ax1.barh(list(Y.keys()), Y.values())
        ax2.barh(list(Z.keys()), Z.values())
        for index,data in enumerate(X.values()):
            ax0.text(x=index , y =data , s=f"{list(X.keys())[index], data}" , fontdict=dict(fontsize=15), 
                     horizontalalignment='center', verticalalignment='bottom')
        for index,data in enumerate(Y.values()):
            ax1.text(x=data , y =index , s=f"{list(Y.keys())[index], data}" , fontdict=dict(fontsize=12), 
                    horizontalalignment='left', verticalalignment='center') 
        for index,data in enumerate(Z.values()):
            ax2.text(x=data , y =index , s=f"{list(Z.keys())[index], data}" , fontdict=dict(fontsize=5), 
                    horizontalalignment='left', verticalalignment='center')  
        ax0.set_xticks([])
        ax1.set_yticks([])
        ax2.set_yticks([])
        ax1.set_xlim(0, list(Y.values())[0]*1.1)
        fig.tight_layout()
        plt.savefig(str(nazwa) + " - symbolizacja.png")
        plt.clf()
        plt.close(fig)
        
        Symbolizacje={"Jednoelementowa": s, "Dwuelementowa": s2, "Trzyelementowa": s3}
        for name, stany in Symbolizacje.items():
            k=0
            lista_stanow={}
            for n in set(stany):
                lista_stanow[n]=k
                for x in range(len(stany)):
                    if stany[x]==n:                        stany[x]=k
                k=k+1
                
            punktA(macierz_przejscia(stany, max(stany)+1), nazwa  + "- RR_" + str(i) + " - Symbolizacja " + name)


# # Wywołanie programu

# In[17]:


def calosc(dekada):
    for i in range(len(dekada)):
        series1 = read_csv(dekada[i], header=0, delimiter = "\t")
        series1.columns = ["Wartości", "index"]
        series1 = series1.set_index('index')
        
        macierz0=macierz_przejscia(zamiana_na_stany(series1, 1), max(zamiana_na_stany(series1, 1))+1)
        lancuchy_markova=zamiana_na_łańcuch(series1)
        
        os.mkdir(str(dekada[i].strip(".txt")) + " folder")
        os.chdir("./" + str(dekada[i].strip(".txt")) + " folder")
        for n in range(len(lancuchy_markova[0])):
            macierz=macierz_przejscia(lancuchy_markova[0][n], max(lancuchy_markova[0][n])+1)
            punktA(macierz, dekada[i].strip(".txt")+" - k="+str(lancuchy_markova[1][n]))
             
        os.mkdir(str(dekada[i].strip(".txt")) + " - zróżnicowania")
        os.chdir("./" + str(dekada[i].strip(".txt")) + " - zróżnicowania")
        punktB(series1, dekada[i].strip(".txt"))
        os.chdir('..')
             
        os.mkdir(str(dekada[i].strip(".txt")) + " - okna")
        os.chdir("./" + str(dekada[i].strip(".txt") + " - okna"))         
        punktC(series1, dekada[i].strip(".txt"))
        os.chdir('..')
        
        os.mkdir(str(dekada[i].strip(".txt")) + " - symbolizacja")
        os.chdir("./" + str(dekada[i].strip(".txt") + " - symbolizacja"))  
        punktD(series1, dekada[i].strip(".txt"))
        os.chdir('..')
        os.chdir('..')


# In[18]:


path = os.getcwd() 
dir_list = os.listdir(path)
dekada=[]
for i in range (0, len(dir_list)):
    if 'm70' in dir_list[i] or 'f70' in dir_list[i]:
        dekada.append(dir_list[i])
calosc(dekada)

