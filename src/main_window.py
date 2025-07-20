#main_window.py
#Ziel: Erstellen ein zuerst Fenster für die Bike Fit Analyzer App und der Programmstart
import sys
import cv2
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QHBoxLayout
)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import QTimer, Qt
from bike_fit_app.videoAnalyse import VideoAnalyzer
from PySide6.QtWidgets import QMessageBox

import Theme # Import the theme module to set dark or light mode
from scipy.signal import savgol_filter # helps fix weird angles


class MainWindow(QWidget):
    def __init__(self):
        self.playing = False
        super().__init__()
        self.setWindowTitle("🚴‍♂️ Bike Fit Analyzer 🚴‍♀️")
        self.setGeometry(400, 100, 800, 600)
        self.video_analyzer = None
        self.current_video_path = None  # Add this line
        self.operationalSystem = Theme.getOS()  # Detect operational system
        self.dark_mode = Theme.is_system_dark(self.operationalSystem)  # Detect system theme
        self.playing = False  # 🔧 Corrige erro de atributo inexistente
        self.initUI()#after these first datas setup, we build the UI(the window)


    def initUI(self):
        layout = QVBoxLayout()#Erstellen layout

        #Label für Videoanzeige
        self.label_video = QLabel("Nenhum vídeo carregado")
        self.label_video.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_video)

        #Tastenlayout QH-> Horizontal
        button_layout = QHBoxLayout()#Hinzufügen eines Layouts für die Tasten 

        #button load
        self.btn_load = QPushButton("📂 Carregar Vídeo")#
        self.btn_load.clicked.connect(self.load_video)#attach function
        button_layout.addWidget(self.btn_load)#insert to loadout

        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        Theme.apply_theme(self, self.dark_mode)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)


    def load_video(self):
        file_dialog = QFileDialog()
        video_path, _ = file_dialog.getOpenFileName(self, "Selecione o vídeo", "", "Videos (*.mp4 *.avi *.mov *.mkv)")

        #Bug Solve: when new file is inserted it used to not start if the old was playing.
        if video_path:
            # 1. Parar o vídeo atual se estiver rodando
            if self.playing:
                self.play_pause_video()  # Isso irá parar o timer


            # 2. Liberar recursos do vídeo anterior
            if self.video_analyzer:            
                self.video_analyzer.release()

            # 3. Criar novo analisador de vídeo
            try:
                self.video_analyzer = VideoAnalyzer(video_path)
                self.label_video.setText("Novo vídeo carregado.")
                
                # 4. Resetar estado de reprodução
                self.playing = False
                self.play_pause_video()  # Inicia o novo vídeo
                
            except Exception as e:
                self.label_video.setText(f"Erro: {str(e)}")
                QMessageBox.critical(self, "Erro", f"Falha ao carregar vídeo:\n{str(e)}")


    def play_pause_video(self):
        if not self.video_analyzer:
            return

        if not self.playing:
            self.playing = True
            self.timer.start(30)  # 30ms ~ 33fps

        else:
            self.playing = False
            self.timer.stop()


    def smooth_angles(self, angles):
        """Add this new method"""
        if not angles or len(angles) < 5:
            return angles
            
        median = np.median(angles)
        mad = 1.4826 * np.median(np.abs(angles - median))
        cleaned = [x if abs(x - median) < 2.5*mad else median for x in angles]
        
        window_size = min(9, len(cleaned))
        if window_size % 2 == 0:
            window_size -= 1
            
        return savgol_filter(cleaned, window_size, 2)

   
    def update_frame(self):
        if not self.video_analyzer or not self.playing:  # Verificação adicional
            return
        
        if self.video_analyzer:
            frame = self.video_analyzer.process_next_frame()
            if frame is None:
                self.playing = False
                self.timer.stop()
                self.gerar_resultados()
                return

            # Conversão de imagem para o QLabel
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            qimg = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg).scaled(800, 450, Qt.KeepAspectRatio)
            self.label_video.setPixmap(pixmap)


    def video_ended(self):
        """Add this new method"""
        self.timer.stop()
        self.btn_load.setEnabled(True)
        
        if self.video_analyzer:
            try:
                knee_angles = self.smooth_angles(self.video_analyzer.angulos_joelho)
                ankle_angles = self.smooth_angles(self.video_analyzer.angulos_tornozelo)
                
                # Conversão de imagem para o QLabel
                height, width, channel = frame.shape
                bytes_per_line = 3 * width
                qimg = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qimg).scaled(800, 450, Qt.KeepAspectRatio)
                self.label_video.setPixmap(pixmap)
                
            except Exception as e:
                QMessageBox.warning(self, "Processing Error", str(e))


    def closeEvent(self, event):
        if self.video_analyzer:
            self.video_analyzer.release()
        event.accept()

    
    #Ziehen Bild
    def draw_image(self):
        try:
            # Load image (replace with your image path)
            pixmap = QPixmap("report/grafico.png")  # Change to your image file
            if pixmap.isNull():
                self.label_video.setText("Image not found!\nPut it in this folder.")
                return
                
            # Scale image to fit while keeping aspect ratio
            pixmap = pixmap.scaled(
                self.label_video.width() - 20, self.label_video.height() - 20, 
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            
            self.label_video.setPixmap(pixmap)
            
        except Exception as e:
            self.label_video.setText(f"Error loading image:\n{str(e)}")
    
    
    def gerar_resultados(self):
        """Gera gráficos e PDF ao final do vídeo"""
        try:
            from Graph import gerar_grafico
            from PDF import gerar_pdf
            
            ang_joelho = self.smooth_angles(self.video_analyzer.angulos_joelho)
            ang_tornozelo = self.smooth_angles(self.video_analyzer.angulos_tornozelo)
            
            # Get the results from gerar_grafico which returns the proper structure
            resultados = gerar_grafico(ang_joelho, ang_tornozelo)
            
            # Add video path to results
            resultados['video'] = self.current_video_path
            
            gerar_pdf(resultados)

            self.label_video.setText("Análise concluída!")
            self.draw_image()
            
        except Exception as e:
            QMessageBox.warning(self, "Aviso", f"Erro ao gerar resultados:\n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())