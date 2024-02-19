import numpy as np
import pandas as pd
from scipy import stats as st

def characterictics(data):
    mean, std, var, median, mi, ma, mode, kw1, kw3 = ([] for a in range(9))
    for name in data:
        series1 = pd.read_csv(name, header=0, delimiter="\t")
        series1.columns = ["values", "index"]
        series1 = series1.set_index('index')
        mean.append(np.mean(series1.values))
        std.append(np.std(series1.values))
        var.append(np.var(series1.values))
        median.append(np.median(series1.values))
        mi.append(np.min(series1.values))
        ma.append(np.max(series1.values))
        mode.append(st.mode(series1.values)[0])
        kw1.append(series1.quantile(q=0.25).values[0])
        kw3.append(series1.quantile(q=0.75).values[0])
    return (np.mean(mean), np.mean(std), np.mean(var), np.mean(mi), np.mean(kw1), np.mean(median), np.mean(kw3),
            np.mean(ma), np.mean(mode))

def podpunktB(F, M):
    df = pd.DataFrame(data={'Charakterystyki': ["Średnia:", "Odchylenie st.:", "Wariancja:", "Minimum:", "Kwartyl 1:",
                                             "Mediana:", "Kwartyl 3:", "Maksimum:", "Moda:"]})
    df.insert(1, 'Kobiety', characterictics(F), True)
    df.insert(2, 'Mężczyźni', characterictics(M), True)
    return df
