import numpy as np
import os
import csv
import matplotlib.pyplot as plt
from keras.models import load_model

def best_expression(x):
    return np.sin((x[0]/1.99 - x[7]**1/np.tan((0.43 - np.cos(np.cos(x[3])) - x[7]))))


#Code beginning: ----------------------------------
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
path = os.getcwd()

with open(path + '/training.csv') as csv_file:
    reader = csv.reader(csv_file)
    x = []
    y = []
    next(reader)
    for row in reader:
        x.append(row[1:9])
        y.append(row[9])

x = np.array(x, dtype=np.float)
y = np.array(y, dtype=np.float)

y_pred = list()

for item in x:
    y_pred.append(best_expression(item))


plt.scatter(y, y_pred)
plt.plot([0, 1], [0, 1], alpha=0.75, color='k')
plt.ylabel('Valores reais')
plt.xlabel('Valores estimados')
plt.title('Grafico da valores reais vs estimados para o algoritmo genetico')
plt.show()

nn_model = load_model(path + '/NN.hdf5')

y_pred2 = nn_model.predict(x)
plt.scatter(y, y_pred2)
plt.plot([0, 1], [0, 1], alpha=0.75, color='k')
plt.ylabel('Valores reais')
plt.xlabel('Valores estimados')
plt.title('Grafico da valores reais vs estimados para a rede neural')
plt.show()
