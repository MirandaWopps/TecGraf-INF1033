#test_video_analyser.py
import pytest
import cv2
import numpy as np
from unittest.mock import MagicMock, patch
from bike_fit_app.videoAnalyse import VideoAnalyzer


#Test 1:  arquivo de extensao invalido ou nao existe.
def test_should_accept_only_video_formats():
    """Testa se aceita apenas formatos de vídeo válidos"""
    with pytest.raises(ValueError):#espera o construtor levantar exceção do tipo ValueError
        VideoAnalyzer("invalid_file.txt")  # Arquivo inválido
    with pytest.raises(ValueError):
        VideoAnalyzer("image.jpg")  # Imagem não é um vídeo
    with pytest.raises(ValueError):
        VideoAnalyzer("audio.mp3")  # Áudio não é um vídeo
    # Teste com um vídeo válido (não deve levantar exceção)
    video_analyzer = VideoAnalyzer("test_data/videoplayback.mp4")
    assert video_analyzer is not None  # Verifica se o objeto foi criado corretamente


#Test 2:
def test_should_process_next_frame():#  caminho relativo abaixo porque damos make test a partir do TEcgraf folder.
    video_analizer = VideoAnalyzer("test_data/videoplayback.mp4")  # Use a valid video file for testing
    frame = video_analizer.process_next_frame()
    assert frame is not None  # Ensure that a frame is returned,  so valid video was sent.
    assert isinstance(frame, np.ndarray)  # Ensure the frame is a numpy array (image)
    #no problem 


#Test 3: We need 3 points in order to calculate angle. What if 1 is missing ?
def test_should_only_calculate_angle_with_three_points():
    with patch('cv2.VideoCapture'):
        analyzer = VideoAnalyzer("dummy.mp4")
        
        # Teste com pontos completos
        assert analyzer.calcular_angulo([0,0], [1,1], [2,0]) is not None
        
        # Teste com pontos faltantes (deve falhar)
        with pytest.raises(Exception):# oq tadps de pontos ele vai fazer um raise exception, istoe, o cod na lin ha 42 vai precisar levantar uma exceção para passar no teste.
            analyzer.calcular_angulo([0,0], None, [2,0])
        
        with pytest.raises(Exception):
            analyzer.calcular_angulo([0,0], [1,1], "invalid")


'''
# Test 4: Is the file
def test_should_validate_coordinate_types():
    with patch('cv2.VideoCapture'):
        analyzer = VideoAnalyzer("dummy.mp4")
        
        # Teste com tipos inválidos
        with pytest.raises(ValueError):
            analyzer.calcular_angulo("text", [1,1], [2,0])
            
        with pytest.raises(ValueError):
            analyzer.calcular_angulo([0,0], {"x":1, "y":1}, [2,0])
'''


# Test 5:
# --- Testes de Cálculo de Ângulos ---
def test_calcular_angulo():
    """Testa o cálculo de ângulos entre pontos"""
    with patch('cv2.VideoCapture'):  # Mock video capture, engana a f() dizendo q há captura 
        analyzer = VideoAnalyzer("dummy.mp4")#nem precisa existir
        
        # Pontos para formar um ângulo de 90 graus
        a = [0, 0]
        b = [0, 1]
        c = [1, 1]
        
        angle = analyzer.calcular_angulo(a, b, c)
        assert pytest.approx(angle, 0.1) == 90.0

# Test 6:
 # --- Testes de Liberação de Recursos ---
def test_release_resources():
    """Testa se libera recursos corretamente"""
    with patch('cv2.VideoCapture') as mock_capture:
        mock_cap = MagicMock()
        mock_capture.return_value = mock_cap
        
        analyzer = VideoAnalyzer("dummy.mp4")
        analyzer.release()
        
        mock_cap.release.assert_called_once()



# Test 7:Subprocess to get OS information.What if the subprocess fails? Like: if(t_pid sub==-1)


#Test 8: A ideia é tentar criar ocilações, ou outliers, buscando não permitir o tratamento dos mesmos.
'''
Aqui está uma lista de títulos/exercícios para você praticar o desenvolvimento do código, organizados por nível de complexidade:
📌 Nível Básico (Fundamentos)

    Validação de Extensão de Arquivo

        Criar função que verifica se extensão está na lista permitida

        Tratar casos como: sem extensão, múltiplos pontos, case sensitive

    Mock Básico de VideoCapture

        Implementar classe mock que simula cv2.VideoCapture

        Deve responder a isOpened(), read(), release()

    Cálculo de Ângulos entre Pontos

        Função que recebe 3 pontos (x,y) e retorna ângulo em graus

        Testar com ângulos conhecidos (0°, 45°, 90°, 180°)

📌 Nível Intermediário (Integração)

    Sistema de Pausa/Continuação

        Implementar lógica que pausa/continua o processamento

        Testar estado interno da classe

    Detecção de Landmarks Falsos

        Criar dados mock para mediapipe.solutions.pose

        Simular diferentes configurações de landmarks

    Gerenciamento de Recursos

        Implementar context manager (enter/exit)

        Garantir que recursos são liberados corretamente

📌 Nível Avançado (Sistema Completo)

    Pipeline de Processamento de Vídeo

        Classe que gerencia:
        ✅ Validação de entrada
        ✅ Processamento frame-a-frame
        ✅ Acúmulo de métricas
        ✅ Geração de saída

    Sistema de Tolerância a Falhas

        Continuar processamento mesmo se:

            Algum frame falhar

            MediaPipe não detectar pose

            Problemas temporários de I/O

    Teste de Integração Realista

        Usar vídeo de teste pequeno (2-3s)

        Verificar:

            Taxa de processamento

            Consistência dos ângulos calculados

            Uso de memória

🛠️ Bônus (Desafios Extras)

    CLI Interativo

        Menu para:
        ▶️ Carregar vídeo
        ⏸️ Pausar/Continuar
        📊 Mostrar métricas
        💾 Exportar resultados

    Visualização em Tempo Real

        Plotar gráfico com ângulos enquanto processa

        Overlay dos landmarks no vídeo

    Multiplataforma

        Adaptar validação para:

            Windows (checar registry)

            Linux (checar gsettings)

            macOS (checar defaults)



'''