import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QSize
import subprocess
import threading
import cv2  # Você precisa importar cv2 para gravação

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚴‍♂️ Bike Fit Analyzer 🚴‍♀️")
        self.setGeometry(500, 200, 400, 400)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title = QLabel("🚴 Bike Fit Analyzer 🚴")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Botão de selecionar vídeo
        btn_analyze = QPushButton("📂 Selecionar Vídeo e Analisar")
        btn_analyze.setFixedHeight(60)
        btn_analyze.clicked.connect(self.select_video)
        layout.addWidget(btn_analyze)

        # Botão de webcam
        self.button_cam = QPushButton("🎥 Webcam")
        self.button_cam.setFixedHeight(60)
        self.button_cam.clicked.connect(self.toggle_recording)
        layout.addWidget(self.button_cam)

        # Botão de estatísticas
        btn_stats = QPushButton("📊 Estatísticas")
        btn_stats.setFixedHeight(60)
        # btn_stats.clicked.connect(self.ver_estatisticas)
        layout.addWidget(btn_stats)

        # Botão de sair
        btn_exit = QPushButton("❌ Sair")
        btn_exit.setFixedHeight(60)
        btn_exit.clicked.connect(self.close)
        layout.addWidget(btn_exit)

        self.setLayout(layout)

        self.recording = False
        self.capture_thread = None

    # Gets file of video.
    def select_video(self):
        file_dialog = QFileDialog()
        video_path, _ = file_dialog.getOpenFileName(self, "Selecione o vídeo", "", "Videos (*.mp4 *.avi *.mov *.mkv)")

        if video_path:
            print(f"Arquivo selecionado: {video_path}")
            subprocess.run(["python3", "videoAnalyse.py", video_path])  # Use python3 se necessário

    # Webcam capture.
    def toggle_recording(self):
        if not self.recording:
            self.recording = True
            self.button_cam.setText("🛑 Parar Gravação")
            self.capture_thread = threading.Thread(target=self.record_video)
            self.capture_thread.start()
        else:
            self.recording = False
            self.button_cam.setText("🎥 Iniciar Gravação")

    def record_video(self):
        cap = cv2.VideoCapture(0)#Abre Webcam
#        cap = cv2.VideoCapture("../../videoplayback.mp4")#Mocking: ausência de webcam.
        if not cap.isOpened():
            print("Erro: Webcam não encontrada ou não pode ser aberta.")
            return  # Sai da função para não tentar gravar
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter('gravado.mp4', fourcc, 20.0, (640, 480))

        while self.recording and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
            cv2.imshow('Gravando...', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.recording = False
                break

        cap.release()
        out.release()
        cv2.destroyAllWindows()
        print("Gravação finalizada. Vídeo salvo como gravado.mp4")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

===================================

