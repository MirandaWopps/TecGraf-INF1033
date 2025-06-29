# generierenGraphen.py
# The matplotlib will work inside qt6 
import matplotlib
matplotlib.use('QtAgg')


import matplotlib.pyplot as plt
import numpy as np



def calcular_mediana_intervalo(valores, limite_inferior, limite_superior):
    """Calcula a mediana dentro de um intervalo do conjunto de dados"""
    valores_intervalo = [v for v in valores if limite_inferior <= v <= limite_superior]
    valores_intervalo.sort()
    n = len(valores_intervalo)
    if n == 0:
        return None  # para segurança
    if n % 2 == 1:
        return valores_intervalo[n // 2]
    else:
        return (valores_intervalo[n // 2 - 1] + valores_intervalo[n // 2]) / 2

def gerar_grafico(angulos_joelho, angulos_tornozelo, caminho_saida='grafico.png', exibir = True):
    """Gera os gráficos com as medianas de máximos e mínimos"""

    # Joelho
    min_j, max_j = np.min(angulos_joelho), np.max(angulos_joelho)
    mediana_max_j = calcular_mediana_intervalo(angulos_joelho, max_j - 0.1*(max_j - min_j), max_j)
    mediana_min_j = calcular_mediana_intervalo(angulos_joelho, min_j, min_j + 0.1*(max_j - min_j))

    # Tornozelo
    min_t, max_t = np.min(angulos_tornozelo), np.max(angulos_tornozelo)
    mediana_max_t = calcular_mediana_intervalo(angulos_tornozelo, max_t - 0.1*(max_t - min_t), max_t)
    mediana_min_t = calcular_mediana_intervalo(angulos_tornozelo, min_t, min_t + 0.1*(max_t - min_t))

    # Plot
    plt.figure(figsize=(10, 5))

    # Joelho
    plt.subplot(1, 2, 1)
    plt.plot(angulos_joelho, label='Joelho')
    plt.axhline(min_j, color='blue', linestyle='--', label='Mínimo')
    plt.axhline(max_j, color='red', linestyle='--', label='Máximo')
    plt.axhline(mediana_max_j, color='red', linestyle='-', label='Mediana Max')
    plt.axhline(mediana_min_j, color='blue', linestyle='-', label='Mediana Min')
    plt.title('Ângulo do Joelho')
    plt.xlabel('Frame')
    plt.ylabel('Ângulo (graus)')
    plt.legend()

    # Tornozelo
    plt.subplot(1, 2, 2)
    plt.plot(angulos_tornozelo, color='orange', label='Tornozelo')
    plt.axhline(min_t, color='blue', linestyle='--', label='Mínimo')
    plt.axhline(max_t, color='red', linestyle='--', label='Máximo')
    plt.axhline(mediana_max_t, color='red', linestyle='-', label='Mediana Max')
    plt.axhline(mediana_min_t, color='blue', linestyle='-', label='Mediana Min')
    plt.title('Ângulo do Tornozelo')
    plt.xlabel('Frame')
    plt.ylabel('Ângulo (graus)')
    plt.legend()

    plt.tight_layout()
    plt.savefig(caminho_saida)
    
    #Se o parametro está True teremos exibicao do grafico na tela.
    if exibir:
        plt.show()
    
    plt.close()

    # Retorna também os valores para o PDF
    return {
        "joelho": {"min": min_j, "max": max_j, "mediana_max": mediana_max_j, "mediana_min": mediana_min_j},
        "tornozelo": {"min": min_t, "max": max_t, "mediana_max": mediana_max_t, "mediana_min": mediana_min_t}
    }
