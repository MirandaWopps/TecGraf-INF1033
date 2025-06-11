import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog
import subprocess

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analisador de Vídeo")
        self.setGeometry(300, 300, 300, 200)
        layout = QVBoxLayout()

        self.button_analyze = QPushButton("Selecionar Vídeo e Analisar")
        self.button_analyze.clicked.connect(self.select_video)
        layout.addWidget(self.button_analyze)

        self.setLayout(layout)

    def select_video(self):
        file_dialog = QFileDialog()
        video_path, _ = file_dialog.getOpenFileName(self, "Selecione o vídeo", "", "Videos (*.mp4 *.avi *.mov *.mkv)")

        if video_path:
            print(f"Arquivo selecionado: {video_path}")

            # Chama o videoAnalyse.py passando o caminho do vídeo como argumento
            subprocess.run(["python", "videoAnalyse.py", video_path])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
