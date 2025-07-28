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


def gerar_grafico(angulos_joelho, angulos_tornozelo, caminho_saida='report/grafico.png'):
    """Gera os gráficos com as medianas de máximos e mínimos"""
    if len(angulos_joelho) == 0 or len(angulos_tornozelo) == 0:
        raise ValueError("Não há dados suficientes para gerar o gráfico")

    # Verificação de dados vazios. Usamos .all() porque são array numpy. Inclusive, para referir se todos angulos existem.
    if not angulos_joelho.all() or not angulos_tornozelo.all():
        raise ValueError("Dados de ângulos vazios")
    
    import os
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)

    #Default value !!!!! Alright !!! FIND THE DEFAULT VALUE THAT INCREASES
    #  WITH EACH PERCENT. What to do ? 
    #  We need min and max of the interval !
    #  defaultValue = (max - min) / 100
    #  intervalMedian = defaultValue * 50
    #  

    # Joelho
    angulos_joelho_minAng = np.min(angulos_joelho) #angulo mínimo do joelho, prcisa disso depois do filtro para saber quem é o novo minimo
    angulos_joelho_maxAng = np.max(angulos_joelho) #angulo máximo  do joelho                     lim inferior                                   lim suṕerior               
    mediana_max_j = calcular_mediana_intervalo(angulos_joelho , angulos_joelho_maxAng,  angulos_joelho_maxAng    - 0.1*(angulos_joelho_maxAng - angulos_joelho_minAng) )
                                            #   vetor de angulos,           A ideia é pegar o ângulo máximo e diminuir 10% do intervalo, para pegar a mediana máxima.

    # Tornozelo
    angulos_tornozelo_minAng = np.min(angulos_tornozelo) #angulo mínimo do tornozelo
    angulos_tornozelo_maxAng  = np.max(angulos_tornozelo)#angulo máximo  do tornozelo
    mediana_max_t = calcular_mediana_intervalo(angulos_tornozelo, angulos_tornozelo_maxAng , angulos_tornozelo_maxAng - 0.1*(angulos_tornozelo_maxAng - angulos_tornozelo_minAng)  )
     

    # Plot
    plt.figure(figsize=(10, 5))#tamanho da figura.

    # Joelho
    plt.subplot(1, 2, 1)# divide em grade (m linhas, n colunas, o primeiro subplot é selecioado)
    plt.plot(angulos_joelho, label='Joelho')
    plt.axhline(angulos_joelho_maxAng, color='red', linestyle='--', label='Máximo')#ahxline desenha
    plt.axhline(mediana_max_j, color='red', linestyle='-', label='Mediana Max')# uma linha.
    plt.title('Ângulo do Joelho')#titulo do grafico
    plt.xlabel('Frame')#Eixo X legenda.
    plt.ylabel('Ângulo (graus)')#Eixo Y legenda.
    plt.legend()#Isso habilita a legenda estar visível.

    # Tornozelo
    plt.subplot(1, 2, 2)
    plt.plot(angulos_tornozelo, color='orange', label='Tornozelo')
    plt.axhline(angulos_tornozelo_maxAng, color='red', linestyle='--', label='Máximo')
    plt.axhline(mediana_max_t, color='red', linestyle='-', label='Mediana Max')
    plt.title('Ângulo do Tornozelo')
    plt.xlabel('Frame')
    plt.ylabel('Ângulo (graus)')
    plt.legend()

    plt.tight_layout()#Isso faz que tudo agregue.

    import os
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)

    plt.savefig(caminho_saida)
    
    #Se o parametro está True teremos exibicao do grafico na tela.

    plt.show()
    plt.close()

    # Retorna também os valores para o PDF
    return {
        "joelho":   {"max": angulos_joelho_maxAng,
                    "mediana_max": mediana_max_j },

        "tornozelo": {"max": angulos_tornozelo_maxAng,
                      "mediana_max": mediana_max_t}
    }