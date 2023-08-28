import matplotlib.pyplot as plt 
import numpy as np

#Alocados a sub_area, area,area desconhecida, proprio trabalho, sem area definida

algoritmo_atual_14 = [1453, 416, 41, 0, 0]
algoritmo_atual_15 = [1290, 434, 24, 0, 0]
algoritmo_atual_16 = [0, 1626, 48, 0, 0]
algoritmo_atual_17 = [1234, 420, 26, 0, 0]


algoritmo_antigo_14 = [1509, 376,25, 0, 0]
algoritmo_antigo_15 = [1331,394,23, 0, 0]
algoritmo_antigo_16 = [0, 1630, 44, 0, 0]
algoritmo_antigo_17 = [1256, 400,24, 0, 0]


nao_otimizado_14 = [1168, 675, 135, 3, 0]
nao_otimizado_15 = [826, 622, 112, 6, 441]
nao_otimizado_16 = [0, 1380, 102, 4, 423]
nao_otimizado_17 = [601, 626, 276, 11, 296]


barWidth = 0.25

plt.figure(figsize=(10, 5))

r1 = np.arange(len(algoritmo_atual_14))
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]

bar_atual =plt.bar(r1, algoritmo_atual_14, color='red', width=barWidth, label='Algoritmo Atual')
bar_antigo = plt.bar(r2, algoritmo_antigo_14, color='orange', width=barWidth, label='Algoritmo Antigo')
bar_nao_otimizado = plt.bar(r3, nao_otimizado_14, color='blue', width=barWidth, label='Algoritmo sem técnicas de otimização')


plt.xticks([r + barWidth for r in range(len(algoritmo_atual_14))], ['Alocados a\nsubárea de\nespecialidade', 'Alocados a\nárea de\nespecialidade', 'Alocados a\numa área\ndesconhecida', 'Alocados ao\npróprio trabalho', 'Sem área\ndefinida'])
# Adicionar os valores exatos no topo das barras

plt.bar_label(bar_atual, fmt="%.01f", size=8, label_type="edge")
plt.bar_label(bar_antigo, fmt="%.01f", size=8, label_type="edge")
plt.bar_label(bar_nao_otimizado, fmt="%.01f", size=8, label_type="edge")

plt.ylabel('Quantidade de avaliadores')
plt.title('Alocação de avaliadores, 2014')
plt.legend()

plt.savefig('barras2014.png', dpi=600)
plt.show()
