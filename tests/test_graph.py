import pytest
import numpy as np
from bike_fit_app.videoAnalyse import VideoAnalyzer


def test_should_compute_median_vales():
    vetor = [150] * 100
    vetor[50] = 180  # por exemplo, a posição 50 recebe 180

    video_analyzer = VideoAnalyzer("test_data/videoplayback.mp4") 

    vetor_outliers = video_analyzer.remover_outliers(vetor)
    assert 180 not in vetor_outliers



#o vetor para gerar o gráfico vem nulo ?
def test_should_have_graph():
# 1. Arrange (Preparação)
    # Cria o analisador com um vídeo de teste que existe
    video_analyzer = VideoAnalyzer("test_data/videoplayback.mp4")
    
    # 2. Act (Ação)
    # Processa todos os frames do vídeo
    while not video_analyzer.stopped:#enquanto o video nao parar
        frame = video_analyzer.process_next_frame()# frame = o output da funcao process_next_frame em video_analyzer
        if frame is None:#se frame for None, PARA
            break
    
    # 3. Assert (Verificação)
    # Verifica se os vetores foram preenchidos "foram criados ?"
    assert video_analyzer.angulos_joelho is not None, "Vetor de ângulos do joelho é None" # é vazio ou nao ?
    assert video_analyzer.angulos_tornozelo is not None, "Vetor de ângulos do tornozelo é None"# idem
    
    # Verifica se os vetores não estão vazios "tem algo no vetor ?"
    assert len(video_analyzer.angulos_joelho) > 0, "Vetor de ângulos do joelho está vazio" # 
    assert len(video_analyzer.angulos_tornozelo) > 0, "Vetor de ângulos do tornozelo está vazio"
    
    # Verifica se contém apenas valores numéricos
    assert all(isinstance(x, (int, float)) for x in video_analyzer.angulos_joelho), "Ângulos do joelho contêm valores não numéricos"
    assert all(isinstance(x, (int, float)) for x in video_analyzer.angulos_tornozelo), "Ângulos do tornozelo contêm valores não numéricos"



#os vetores estão sendo aparados de abaixo de 60% ?
def test_should_filter_angles_above_60_percent():
    # 1. Arrange (Preparação)
    video_analyzer = VideoAnalyzer("test_data/videoplayback.mp4")
    
    # 2. Act (Ação)
    while not video_analyzer.stopped:
        frame = video_analyzer.process_next_frame()
        if frame is None:
            break
    
    # 3. Assert (Verificação)
    media_joelho = np.mean(video_analyzer.angulos_joelho)
    media_tornozelo = np.mean(video_analyzer.angulos_tornozelo)

    assert all(angle >= 0.6 * media_joelho for angle in video_analyzer.angulos_joelho), "Ângulos do joelho abaixo de 60% da média"
    assert all(angle >= 0.6 * media_tornozelo for angle in video_analyzer.angulos_tornozelo), "Ângulos do tornozelo abaixo de 60% da média"