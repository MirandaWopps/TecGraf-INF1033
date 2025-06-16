import sys
import cv2
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap

class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_frame)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Simple Video Player")

        self.video_label = QLabel("Selecione um vídeo")
        self.video_label.setAlignment(Qt.AlignCenter)

        self.btn_open = QPushButton("Abrir")
        self.btn_open.clicked.connect(self.open_file)

        self.btn_play = QPushButton("Play")
        self.btn_play.clicked.connect(self.play_video)
        self.btn_play.setEnabled(False)

        self.btn_pause = QPushButton("Pause")
        self.btn_pause.clicked.connect(self.pause_video)
        self.btn_pause.setEnabled(False)

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.btn_open)
        layout.addWidget(self.btn_play)
        layout.addWidget(self.btn_pause)

        self.setLayout(layout)

    def open_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Selecione o vídeo", "", "Videos (*.mp4 *.avi *.mov *.mkv)")
        if file_path:
            self.cap = cv2.VideoCapture(file_path)
            self.btn_play.setEnabled(True)
            self.btn_pause.setEnabled(True)

    def play_video(self):
        self.timer.start(33)  # 30 fps

    def pause_video(self):
        self.timer.stop()

    def next_frame(self):
        if self.cap:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, channel = frame.shape
                q_img = QImage(frame.data, width, height, 3 * width, QImage.Format_RGB888)
                self.video_label.setPixmap(QPixmap.fromImage(q_img).scaled(
                    self.video_label.width(), self.video_label.height(), Qt.KeepAspectRatio
                ))
            else:
                self.timer.stop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec())
