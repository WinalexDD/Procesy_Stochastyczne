from A_a import punktA


def punktB(K, nazwa):
    for i in range(1, 21):
        s = K.diff(periods=i).dropna()
        punktA(s, str(nazwa) + " - RR_" + str(i))
