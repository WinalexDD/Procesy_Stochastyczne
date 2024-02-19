from pandas import DataFrame
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
import numpy as np
from scipy import stats as st
from statsmodels.sandbox.stats.runs import runstest_1samp


def punktA(K, nazwa):
    def missing_indexes(K):
        brakujace_indexy = []
        for i in range(len(K.index) - 1):
            if np.diff(K.index)[i] != 1:
                for n in range(1, np.diff(K.index)[i]):
                    brakujace_indexy.append(K.index[i] + n)
        if brakujace_indexy:
            braki = []
            m = [brakujace_indexy[0]]
            for k in range(len(brakujace_indexy) - 1):
                if brakujace_indexy[k + 1] - brakujace_indexy[k] != 1:
                    m.append(brakujace_indexy[k])
                    m.append(brakujace_indexy[k + 1])
            m.append(brakujace_indexy[-1])
            for n in range(0, len(m), 2):
                braki.append(str(m[n]) + " - " + str(m[n + 1]))
            return "Brakuje " + str(len(brakujace_indexy)) + " indeksów", braki
        else:
            return "Nie ma brakujących indeksów", []

    wartosci = K.values
    result1 = adfuller(K)
    wartkryt = dict()
    A = result1[4]
    for key in A:
        wartkryt[key] = round(A[key], 3)

    M = []
    X = wartosci.tolist()
    for i in range(len(wartosci)):
        M.append(X[i][0])
    result2 = runstest_1samp(M)

    def wniosek1(a):
        if a[1] > 0.05:
            return "Przyjmujemy H0, że seria nie jest stacjonarna"
        else:
            return "Przyjmujemy H1, że seria jest stacjonarna"

    def wniosek2(a):
        if a[1] > 0.05:
            return "Przyjmujemy H0, że dane są losowe"
        else:
            return "Przyjmujemy H1, że dane nie są losowe"

    df = DataFrame(data={'Charakterystyki': ["Kompletność:", "Brakujące indeksy to:",
                                             "Średnia:", "Wariancja:", "Mediana:", "Wartość mody:",
                                             "Ilość wystąpień mody:", "Minimum:", "Maksimum:",
                                             "Test ADF - statystyka:", "Test ADF - p-wartość:",
                                             "Test ADF - wartości krytyczne:", "Test ADF - interpretacja:",
                                             "Test WW - statystyka:", "Test WW - p-wartość:",
                                             "Test WW - interpretacja:"],
                         'Wartości': [missing_indexes(K)[0], missing_indexes(K)[1],
                                      np.mean(wartosci), np.var(wartosci), np.median(wartosci),
                                      int(st.mode(wartosci)[0][0]),
                                      int(st.mode(wartosci)[1][0]), np.min(wartosci), np.max(wartosci),
                                      result1[0], result1[1],
                                      wartkryt, wniosek1(result1),
                                      result2[0], result2[1], wniosek2(result2)]})

    plt.rcParams["figure.figsize"] = (3, 3)
    fig, ax = plt.subplots()
    fig.patch.set_visible(False)
    ax.axis('off')
    tabelawykres = plt.table(cellText=df.values, cellLoc='center', rowLabels=df.index, colLabels=df.columns,
                             loc='center')
    tabelawykres.set_fontsize(50)
    plt.gcf().set_size_inches(50, 50)
    plt.savefig(str(nazwa) + ' - tabela.png')
    plt.close()

    plt.rcParams["figure.figsize"] = (15, 15)
    ax = K.plot()
    plt.axhline(float(np.mean(K)), color='r', linestyle='-', label="Średnia")
    plt.scatter([K.idxmin(), K.idxmax()], [np.min(K.values), np.max(K.values)], color="red", s=50)
    plt.annotate(str(round(np.mean(K.values), 3)), (np.min(K.index) +
                                                    int(len(K) / 2), np.mean(K.values) + 5), fontsize=20)
    plt.annotate(str(np.min(K.values)), (K.idxmin(), np.min(K.values) + 5), fontsize=20)
    plt.annotate(str(np.max(K.values)), (K.idxmax(), np.max(K.values) + 5), fontsize=20)
    plt.legend()
    ax.figure.savefig(str(nazwa) + ' - wykres1.png')
    for i, szerokosc in enumerate([10, 15, 20, 25]):
        ax = plt.subplot(2, 2, i + 1)
        ax.hist(K.values, bins=szerokosc, edgecolor='black')
        ax.set_title('Ilość przedziałów = %d' % szerokosc, color="red")
        ax.set_xticks(
            range(int(np.min(K.values)), int(np.max(K.values)), int((np.max(K.values) - np.min(K.values)) / szerokosc)))
        ax.set_xticklabels(range(int(np.min(K.values)), int(np.max(K.values)),
                                 int((np.max(K.values) - np.min(K.values)) / szerokosc)), fontsize=13,
                           rotation='vertical')
        ax.tick_params(axis='x', colors='red')
        ax.tick_params(axis='y', colors='red')
    plt.savefig(str(nazwa) + ' - wykres2.png')
    plt.close()
