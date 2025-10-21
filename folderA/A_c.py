import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.sandbox.stats.runs import runstest_1samp
from pandas import concat, DataFrame


def punktC(K, nazwa):
    K = K.dropna()
    df1 = []
    for i in range(20, 210, 10):
        mean, var, median, mi, ma, adf, pval1, ww, pval2, stacjo, niestacjo = ([] for _ in range(11))
        for n in range(int(len(K) / i)):
            x = K.values[n * i:n * i + i].tolist()
            mean.append(np.mean(x))
            var.append(np.var(x))
            median.append(np.median(x))
            mi.append(np.min(x))
            ma.append(np.max(x))
            X = adfuller(x)
            adf.append(X[0])
            pval1.append(X[1])
            if X[1] > 0.05:
                niestacjo.append(1)
            else:
                stacjo.append(1)
            M = []
            for m in range(len(x)):
                M.append(x[m][0])
            Y = runstest_1samp(M)
            ww.append(Y[0])
            pval2.append(Y[1])
        stac = len(stacjo) / int(len(K) / i) * 100
        nstac = len(niestacjo) / int(len(K) / i) * 100

        df1.append(DataFrame({'Rozmiar okna': [i],
                              'Średnia': [round(np.mean(mean), 3)],
                              'Wariancja': [round(np.mean(var), 3)],
                              'Mediana': [round(np.mean(median), 3)],
                              'Minimum': [round(np.mean(mi), 3)],
                              'Maksimum': [round(np.mean(ma), 3)],
                              'Stat. ADF': [round(np.mean(adf), 3)],
                              'p-value ADF': [round(np.mean(pval1), 3)],
                              'Stat. WW': [round(np.mean(ww), 3)],
                              'p-value WW': [round(np.mean(pval2), 3)],
                              "% okien st.": [round(stac, 3)],
                              '% okien niest.': [round(nstac, 3)]}))

        fig, (ax0, ax1) = plt.subplots(nrows=2, ncols=1, figsize=(15, 20))
        ax0.plot(mean, label='Średnia')
        ax0.plot(var, label='Wariancja')
        ax0.plot(median, label='Mediana')
        ax0.plot(mi, label='Minimum')
        ax0.plot(ma, label='Maksimum')
        ax0.legend()
        ax0.tick_params(axis='x', colors='red')
        ax0.tick_params(axis='y', colors='red')
        ax1.plot(adf, label='Statystyka ADF')
        ax1.plot(ww, label='Statystyka WW')
        ax1.plot(pval1, label='p-value ADF')
        ax1.plot(pval2, label='p-value WW')
        ax1.legend()
        ax1.tick_params(axis='x', colors='red')
        ax1.tick_params(axis='y', colors='red')
        fig.suptitle("Wykresy dla okien o rozmiarze " + str(i))
        plt.savefig(str(nazwa) + " okno rozmiaru " + str(i) + ' - wykresy statystyk.png')
        plt.close(fig)

    df = concat([df1[i] for i in range(len(df1))],
                ignore_index=True)
    df = df.set_index('Rozmiar okna')
    plt.rcParams["figure.figsize"] = (5, 5)
    fig, ax = plt.subplots()
    fig.patch.set_visible(False)
    ax.axis('off')
    tabelawykres = plt.table(cellText=df.values, cellLoc='center', rowLabels=df.index, colLabels=df.columns,
                             loc='center')
    tabelawykres.set_fontsize(30)
    plt.gcf().set_size_inches(30, 10)
    tabelawykres.add_cell(0, -1, tabelawykres[0, 1].get_width(), tabelawykres[0, 1].get_height(), text='Rozmiar')
    plt.title("Tabela statystyk dla okien", color="red", fontsize=40)
    plt.savefig(str(nazwa) + ' - tabela.png')
    plt.close()
