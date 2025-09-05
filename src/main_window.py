#main_window.py
#Goal: Erstellen ein zuerst Fenster für die Bike Fit Analyzer App und der Programmstart
import sys
import cv2
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QHBoxLayout
)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import QTimer, Qt
from bike_fit_app.videoAnalyse import VideoAnalyzer
from PySide6.QtWidgets import QMessageBox, QFileDialog 

import Theme # Import the theme module to set dark or light mode
from bike_fit_app.Graph import gerar_grafico #Esse módulo gera o gráfico. Poderia ficar lá em baixo, mas é programa pequeno, então, não atrapalha execução.
from scipy.signal import find_peaks #Adquire máximos locais dos angulos.

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

        #Label for VideoAnalyze
        self.label_video = QLabel("Nenhum vídeo carregado")
        self.label_video.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_video)

        #ButtonLayout QH-> Horizontal
        button_layout = QHBoxLayout()#Add a layout for the Button 

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
        video_path, _ = QFileDialog.getOpenFileName(self, "Selecione o vídeo", "", "Videos (*.mp4 *.avi *.mov *.mkv)")

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

            return 
            
        except Exception as e:
            self.label_video.setText(f"Error loading image:\n{str(e)}")
    
    
    def gerar_resultados(self):
        """Gera gráficos e PDF ao final do vídeo"""
        try:
            if not self.video_analyzer or len(self.video_analyzer.angulos_joelho) == 0:
                raise ValueError("Nenhum dado de ângulo disponível para análise")
            print(f"Total de frames processados - Joelho: {len(self.video_analyzer.angulos_joelho)}, Tornozelo: {len(self.video_analyzer.angulos_tornozelo)}")

            # Converter para arrays numpy
            ang_joelho = np.array(self.video_analyzer.angulos_joelho)
            ang_tornozelo = np.array(self.video_analyzer.angulos_tornozelo)

            # Voce precisa da média dos máximos locais !
            # Índices e propriedades
            indices_joelho, props_joelho = find_peaks(ang_joelho, height=155, distance=10)
            indices_tornozelo, props_tornozelo = find_peaks(ang_tornozelo, height=140, distance=10)

            # Extrair apenas os ângulos correspondentes aos picos
            vJoelhoMaximosLocais = ang_joelho[indices_joelho]
            vTornozeloMaximosLocais = ang_tornozelo[indices_tornozelo]


            # Você precisa dizer ao usuário, de alguma forma, para descer(media > 155) ou subir(media < 140) o banco.
            # A média está vindo lá em gera graph. Use ela para responder ao usuário.
            

            # Escolher dados para plotar
            if len(vJoelhoMaximosLocais) > 0 and len(vTornozeloMaximosLocais) > 0:
                dados_joelho = vJoelhoMaximosLocais
                dados_tornozelo = vTornozeloMaximosLocais
                print("Usando picos máximos locais para análise.")
            else:
                dados_joelho = ang_joelho
                dados_tornozelo = ang_tornozelo
                print("Aviso: Nenhum pico detectado, usando todos os dados.")


            #shall i 


            # Gerar gráfico
            gerar_grafico(dados_joelho, dados_tornozelo)

            # ---- Recomendação de ajuste do banco ----
            media_joelho = np.mean(dados_joelho)
            media_tornozelo = np.mean(dados_tornozelo)
            recomendacao = ""
            if media_joelho > 155:
                recomendacao += "O banco parece alto demais, considere descer um pouco.\n"
            elif media_joelho < 140:
                recomendacao += "O banco parece baixo demais, considere subir um pouco.\n"
            else:
                recomendacao += "A altura do banco está adequada.\n"

            print(f"Média Joelho: {media_joelho:.2f}° | Média Tornozelo: {media_tornozelo:.2f}°")
            print(recomendacao)
        
            self.draw_image()
            
        except Exception as e:
            import traceback
            traceback.print_exc()  # Isso mostrará o traceback completo no console
            QMessageBox.critical(self, "Erro", f"Falha ao gerar resultados: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())