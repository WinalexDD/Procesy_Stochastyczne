import os
from pandas import read_csv
from A_a import punktA
from A_b import punktB
from A_c import punktC
from A_d import punktD


def podpunktA(dekada):
    for i in range(len(dekada)):
        series1 = read_csv(dekada[i], header=0, delimiter="\t")
        series1.columns = ["Wartości", "index"]
        series1 = series1.set_index('index')

        if not os.path.isdir(str(dekada[i].strip(".txt")) + " folder"):
            os.mkdir(str(dekada[i].strip(".txt")) + " folder")
        os.chdir("./" + str(dekada[i].strip(".txt")) + " folder")
        punktA(series1, dekada[i].strip(".txt"))

        if not os.path.isdir(str(dekada[i].strip(".txt")) + " - zróżnicowania"):
            os.mkdir(str(dekada[i].strip(".txt")) + " - zróżnicowania")
        os.chdir("./" + str(dekada[i].strip(".txt")) + " - zróżnicowania")
        punktB(series1, dekada[i].strip(".txt"))
        os.chdir('..')

        if not os.path.isdir(str(dekada[i].strip(".txt")) + " - okna"):
            os.mkdir(str(dekada[i].strip(".txt")) + " - okna")
        os.chdir("./" + str(dekada[i].strip(".txt") + " - okna"))
        punktC(series1, dekada[i].strip(".txt"))
        os.chdir('..')

        punktD(series1, dekada[i].strip(".txt"))
        os.chdir('..')
