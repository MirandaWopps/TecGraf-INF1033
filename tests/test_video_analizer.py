#test_video_analyser.py
import pytest
import cv2
import numpy as np
from unittest.mock import MagicMock, patch
from bike_fit_app.videoAnalyse import VideoAnalyzer


#Test 1
def test_should_accept_only_video_formats():
    """Testa se aceita apenas formatos de vídeo válidos"""
    with pytest.raises(ValueError):#espera o construtor levantar exceção do tipo ValueError
        VideoAnalyzer("invalid_file.txt")  # Arquivo inválido
    with pytest.raises(ValueError):
        VideoAnalyzer("image.jpg")  # Imagem não é um vídeo
    with pytest.raises(ValueError):
        VideoAnalyzer("audio.mp3")  # Áudio não é um vídeo
    # Teste com um vídeo válido (não deve levantar exceção)
    video_analyzer = VideoAnalyzer("/home/lucas/inf1033/TecGraf-INF1033/test_data/videoplayback.mp4")
    assert video_analyzer is not None  # Verifica se o objeto foi criado corretamente



#Test 2:
def test_should_process_next_frame():
    video_analizer = VideoAnalyzer("/home/lucas/inf1033/TecGraf-INF1033/test_data/videoplayback.mp4")  # Use a valid video file for testing
    frame = video_analizer.process_next_frame()
    assert frame is not None  # Ensure that a frame is returned
    assert isinstance(frame, np.ndarray)  # Ensure the frame is a numpy array (image)
    #no problem 

#remover talvez \/ o tst 3 e 4
'''
# Test 3:
def test_process_next_frame_when_paused():
    """Testa comportamento quando pausado"""
    analyzer = VideoAnalyzer("dummy.mp4")
    analyzer.paused = True
    assert analyzer.process_next_frame() is None

# Test 4:
def test_process_next_frame_when_stopped():
    """Testa comportamento quando vídeo acabou"""
    analyzer = VideoAnalyzer("dummy.mp4")
    analyzer.stopped = True
    assert analyzer.process_next_frame() is None
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