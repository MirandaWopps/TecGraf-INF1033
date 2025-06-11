import cv2
from .process import process_frame
from gui.results_view import show_results

def analyze_video(file_path):
    cap = cv2.VideoCapture(file_path)
    if not cap.isOpened():
        print("Erro ao abrir o vídeo.")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = process_frame(frame)
        cv2.imshow("Análise de Vídeo", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
#regerar p mosttrar video edialogo novo. o problema era uma dialogo para cada frame. MUDA ISSO


def analyze_webcam():
    pass



from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

results_window = None  # variável global para manter a janela viva

def show_results():
    global results_window
    if results_window is None:
        results_window = QWidget()
        results_window.setWindowTitle("Resultados da Análise")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Gráficos e métricas apareceriam aqui."))
        results_window.setLayout(layout)
        results_window.resize(400, 300)
    results_window.show()
