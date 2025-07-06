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

import subprocess #acess to terminal
import os #discover the operational system

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚴‍♂️ Bike Fit Analyzer 🚴‍♀️")
        self.setGeometry(400, 100, 800, 600)
        self.video_analyzer = None
        self.operationalSystem = self.getOS()  # Detect operational system
        self.dark_mode = self.is_system_dark(self.operationalSystem)  # Detect system theme
        self.initUI()


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
        self.update_theme()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.playing = False


    def getOS(self): #Discovering the operational system
        if sys.platform.startswith('win'):
            return 'Windows'
        elif sys.platform.startswith('linux'):
            return 'Linux'
        elif sys.platform.startswith('darwin'):
            return 'macOS'
        else:
            return 'Unknown'
    

    #Detecting the system theme
    def is_system_dark(self, os_name):
        if os_name == 'Windows':
            import ctypes
            import winreg
            try:
                # Method 1: System color check
                if ctypes.windll.user32.GetSysColor(15) < 128:  # COLOR_WINDOW = 15
                    return True
                
                # Method 2: Registry check (more reliable)
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize") as key:
                    apps_use_light = winreg.QueryValueEx(key, "AppsUseLightTheme")[0]
                    return apps_use_light == 0
            except Exception as e:
                print(f"Error checking dark mode: {e}")
                return False

        #Linux detection algorithm using a subprocess: a terminal command    
        elif os_name == 'Linux':
            try:
                result = subprocess.run(
                    ["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"],
                    capture_output=True,
                    text=True
                        )
                output = result.stdout.strip()
                if 'prefer-dark' in output:
                    print("a")
                    return True
            except Exception as e:
                print(f"Erro ao detectar tema do sistema: {e}")
                return False
        '''
        palette = self.palette()
        return palette.window().color().lightness() < 128
        '''

    def load_video(self):
        file_dialog = QFileDialog()
        video_path, _ = file_dialog.getOpenFileName(self, "Selecione o vídeo", "", "Videos (*.mp4 *.avi *.mov *.mkv)")

        if video_path:
            self.video_analyzer = VideoAnalyzer(video_path)
            self.label_video.setText("Vídeo carregado.")
            # Inicia o vídeo automaticamente
            self.play_pause_video()



    def play_pause_video(self):
        if not self.video_analyzer:
            return

        if not self.playing:
            self.playing = True
            self.timer.start(30)  # 30ms ~ 33fps

        else:
            self.playing = False
            self.timer.stop()

   
    def update_frame(self):
        if self.video_analyzer:
            frame = self.video_analyzer.process_next_frame()
            if frame is None:
                self.playing = False
                self.timer.stop()

                # --- Geração de gráfico e PDF ao final ---
                from generierenGraphen import gerar_grafico
                from generierenPDF import gerar_pdf
 
                ang_joelho = self.video_analyzer.angulos_joelho
                ang_tornozelo = self.video_analyzer.angulos_tornozelo

                valores = gerar_grafico(ang_joelho, ang_tornozelo)
                
                gerar_pdf(valores)

                print("✅ Gráfico e PDF gerados com sucesso!")
                
                #    Zeigt Graphen Bild
                self.draw_image()
                return

            # Conversão de imagem para o QLabel
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            qimg = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg).scaled(800, 450, Qt.KeepAspectRatio)
            self.label_video.setPixmap(pixmap)


    # Update UI theme
    def update_theme(self):
        """Update UI theme based on current mode"""
        if self.dark_mode:
            self.setStyleSheet("""
                QWidget {
                    background-color: #2D2D2D;
                    color: #FFFFFF;
                }

                QPushButton {
                    background-color: #3A3A3A;
                    border: 1px solid #555;
                    padding: 8px;
                    min-width: 120px;
                    border-radius: 4px;  /* 👈 quanto maior, mais arredondado */
                }
                QPushButton:hover {
                    background-color: #2A2A2A;  /* 👈 Mais escuro ao passar o mouse */
                }
                QLabel {
                    background-color: #3A3A3A;                               
                    border: 1px solid #555;
                    background-color: #2D2D2D;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: #F5F5F5;
                    color: #000000;
                }
                QPushButton {
                    background-color: #E0E0E0;
                    border: 1px solid #AAA;
                    padding: 8px;
                    min-width: 120px;
                    border-radius: 4px;  /* 👈 quanto maior, mais arredondado */
                }
                QLabel {
                    border: 1px solid #AAA;
                }
            """)

    def closeEvent(self, event):
        if self.video_analyzer:
            self.video_analyzer.release()
        event.accept()

    
    #Ziehen Bild
    def draw_image(self):
        try:
            # Load image (replace with your image path)
            pixmap = QPixmap("grafico.png")  # Change to your image file
            if pixmap.isNull():
                self.image_label.setText("Image not found!\nPut it in this folder.")
                return
                
            # Scale image to fit while keeping aspect ratio
            pixmap = pixmap.scaled(
                self.label_video.width() - 20, self.label_video.height() - 20, 
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            
            self.label_video.setPixmap(pixmap)
            
        except Exception as e:
            self.label_video.setText(f"Error loading image:\n{str(e)}")
    
    
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

