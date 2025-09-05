# Graph.py
# The matplotlib will work inside qt6 
import matplotlib
matplotlib.use('QtAgg')

import matplotlib.pyplot as plt #Plot library
import numpy as np #Numpy library for numerical operations
import os
os.makedirs('report', exist_ok=True)  # Cria a pasta se não existir

def calcular_mediana_intervalo(valores, limite_superior, limite_inferior):
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


#Funcao resposnavel por gerar o grafico a partir dos angulos recebidos. "main_window.py" faz o tratamento para obter os máximos locais.
def gerar_grafico(angulos_joelho, angulos_tornozelo, caminho_saida='report/grafico.png'):#esse caminho de saida
    #angulos_joelho    = np.array(angulos_joelho)                                          deixará o gráfico no
    #angulos_tornozelo = np.array(angulos_tornozelo)                                       caminho especificado.
    
    """Gera os gráficos com as medianas de máximos e mínimos"""
    if len(angulos_joelho) == 0 or len(angulos_tornozelo) == 0:
        print("Aviso: Nenhum pico detectado, usando todos os dados.")
        raise ValueError("Não há dados suficientes para gerar o gráfico")


    # Verificação de dados vazios. Usamos .all() porque são array numpy. Inclusive, para referir se todos angulos existem.
    # ✅ Corrigido
    if angulos_joelho is None or len(angulos_joelho) == 0 \
       or angulos_tornozelo is None or len(angulos_tornozelo) == 0:
        raise ValueError("Não há dados suficientes para gerar o gráfico")
    
    import os
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)


    # Joelho | Tornozelo   ->  MEDIANAS
    joelho_mediana    = np.mean(angulos_joelho) #angulo mínimo do joelho, prcisa disso depois do filtro para saber quem é o novo minimo
    tornozelo_mediana = np.mean(angulos_tornozelo) #angulo máximo  do joelho                     lim inferior                                   lim superior               


    # Plot
    plt.figure(figsize=(10, 5))#tamanho da figura.

    # Joelho
    plt.subplot(1, 2, 1)# divide em grade (m linhas, n colunas, o primeiro subplot é selecioado)
    plt.plot(angulos_joelho, label='Joelho')
    plt.axhline(joelho_mediana, color='red', linestyle='-', label='Mediana')# uma linha.
    plt.title('Ângulo do Joelho')#titulo do grafico
    plt.xlabel('Frame')#Eixo X legenda.
    plt.ylabel('Ângulo (graus)')#Eixo Y legenda.
    plt.legend()#Isso habilita a legenda estar visível.

    # Tornozelo
    plt.subplot(1, 2, 2)
    plt.plot(angulos_tornozelo, color='orange', label='Tornozelo')
    plt.axhline(tornozelo_mediana, color='red', linestyle='-', label='Mediana')
    plt.title('Ângulo do Tornozelo')
    plt.xlabel('Frame')
    plt.ylabel('Ângulo (graus)')
    plt.legend()

    plt.tight_layout()#Isso faz que tudo agregue.

    import os
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    plt.savefig(caminho_saida)
    plt.show()
    plt.close()

    return {}