#test_video_analyser.py
import pytest
import cv2
import numpy as np
from unittest.mock import MagicMock, patch
from bike_fit_app.videoAnalyse import VideoAnalyzer

def test_should_accept_only_video_formats():
    # todo: descobrir como testar se levanta um erro
    #Testing video path existance.
    try:
        video_analizer = VideoAnalyzer("path_to_some_png.png") # deve fazer um raise Exception
        assert False
    except Exception:
        assert True


#Test 2:
def test_should_process_next_frame():
    video_analizer = VideoAnalyzer("/home/lucas/inf1033/TecGraf-INF1033/test_data/videoplayback.mp4")  # Use a valid video file for testing
    frame = video_analizer.process_next_frame()
    assert frame is not None  # Ensure that a frame is returned
    assert isinstance(frame, np.ndarray)  # Ensure the frame is a numpy array (image)


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

# Test 5:
# --- Testes de Cálculo de Ângulos ---
def test_calcular_angulo():
    """Testa o cálculo de ângulos entre pontos"""
    analyzer = VideoAnalyzer("dummy.mp4")
    
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