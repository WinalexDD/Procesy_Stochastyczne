import os
import matplotlib.pyplot as plt
from B import podpunktB

# Inputting path to folder with data
datapath = input("Prosze podać ścieżke z katalogiem healthy_decades: ")
os.chdir(str(datapath))

# Getting the list of individual files from chosen decade
path = os.getcwd()
dir_list = os.listdir(path)
dekadaM, dekadaF = [], []
for i in range(0, len(dir_list)):
    if 'm70' in dir_list[i]:
        dekadaM.append(dir_list[i])
    elif 'f70' in dir_list[i]:
        dekadaF.append(dir_list[i])

# Initializing point B and
df = podpunktB(dekadaF, dekadaM)

# Creating folder to save results
if not os.path.isdir("Dekada 70 - kobiety a mężczyzni"):
    os.mkdir("Dekada 70 - kobiety a mężczyzni")
os.chdir("Dekada 70 - kobiety a mężczyzni")

# Saving the table to .png file
plt.rcParams["figure.figsize"] = (3, 3)
fig, ax = plt.subplots()
fig.patch.set_visible(False)
ax.axis('off')
tabelawykres = plt.table(cellText=df.values, cellLoc='center', rowLabels=df.index,
                         colLabels=df.columns, loc='center')
tabelawykres.set_fontsize(50)
plt.gcf().set_size_inches(50, 50)
plt.savefig("Kobiety a mężczyzni tabela.png")
plt.close()
os.chdir('..')
