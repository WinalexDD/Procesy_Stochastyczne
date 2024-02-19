from collections import Counter, OrderedDict
import matplotlib.pyplot as plt


def punktD(K, nazwa):
    RR_1 = K.diff().dropna().values.tolist()
    RR_1_1 = []
    for i in range(len(RR_1)):
        if RR_1[i][0] > 0:
            if 40 > abs(RR_1[i][0]) > 0:
                RR_1[i] = "d"
            else:
                RR_1[i] = "D"
        elif RR_1[i][0] == 0:
            RR_1[i] = "Z"
        else:
            if 40 > abs(RR_1[i][0]) > 0:
                RR_1[i] = "a"
            else:
                RR_1[i] = "A"
        if i % 2 == 1:
            RR_1_1.append(RR_1[i - 1] + RR_1[i])

    X = OrderedDict(Counter(RR_1).most_common())
    Y = OrderedDict(Counter(RR_1_1).most_common())
    fig, (ax0, ax1) = plt.subplots(nrows=2, ncols=1, figsize=(20, 15))
    ax0.bar(list(X.keys()), X.values())
    ax1.barh(list(Y.keys()), Y.values())
    for index, data in enumerate(X.values()):
        ax0.text(x=index, y=data, s=f"{list(X.keys())[index], data}", fontdict=dict(fontsize=20),
                 horizontalalignment='center', verticalalignment='bottom')
    for index, data in enumerate(Y.values()):
        ax1.text(x=data, y=index, s=f"{list(Y.keys())[index], data}", fontdict=dict(fontsize=15),
                 horizontalalignment='left', verticalalignment='center')

    ax0.set_xticks([])
    ax1.set_yticks([])
    ax1.set_xlim(0, list(Y.values())[0] * 1.1)
    fig.tight_layout()
    plt.savefig(str(nazwa) + " - symbolizacja.png")
    plt.close(fig)
