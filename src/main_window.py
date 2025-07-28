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

    '''
    def smooth_angles(self, angles):
        """Suaviza os ângulos usando filtro Savitzky-Golay"""
        if not angles or len(angles) < 5:
            return angles

        #used to be commented
        median = np.median(angles)
        mad = 1.4826 * np.median(np.abs(angles - median))
        cleaned = [x if abs(x - median) < 2.5*mad else median for x in angles]
        #used to be comented

        angles = np.array(angles)  # Garante que é um array numpy
        window_size = min(9, len(angles))
        if window_size % 2 == 0:
            window_size -= 1
            
        return savgol_filter(angles, window_size, 2).tolist()  # Retorna como lista
    '''
   
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

            '''
            # Remover outliers
            ang_j_filtrado = self.video_analyzer.remover_outliers(ang_j)
            ang_t_filtrado = self.video_analyzer.remover_outliers(ang_t)
            '''

            # Suavizar
            ang_j_suavizado = self.video_analyzer.suavizar_angulos(ang_joelho)
            ang_t_suavizado = self.video_analyzer.suavizar_angulos(ang_tornozelo)

            from bike_fit_app.Graph import gerar_grafico
            from PDF import gerar_pdf

            # Get the results from gerar_grafico which returns the proper structure
            #    necessário tratar os ângulos. Obtemos a media
            joelho_angs_media    = np.mean(ang_j_suavizado)
            tornozelo_angs_media = np.mean(ang_t_suavizado)

            print(f"joelho_angs_media: {joelho_angs_media:.2f}, tornozelo_angs_media: {tornozelo_angs_media:.2f}")
            #    para conseguir dizer o filtro.
            interval_joelho = np.max(ang_j_suavizado) - np.min(ang_j_suavizado)
            print(f"Intervalo Joelho: {interval_joelho:.2f}")
            joelho_angs_limite = joelho_angs_media + interval_joelho * 0.1
            
            tornozelo_angs_limite = 0.6 * tornozelo_angs_media

            print(f"joelho_angs_limite: {joelho_angs_limite:.2f}, tornozelo_angs_limite: {tornozelo_angs_limite:.2f}")
            #    E obtemos os angulos que estão acima do limite
            vAngulos_joelho_Maximos    = ang_j_suavizado[ang_j_suavizado > joelho_angs_limite]
            vAngulos_tornozelo_Maximos = ang_t_suavizado[ang_t_suavizado > tornozelo_angs_limite]

            #Debug pós filtro, logo, a quantidade de angulos que sobraram.
            print(f"Angulos Joelho:    {len(ang_j_suavizado)}, {len(vAngulos_joelho_Maximos)}   ")

            for i, angulo in enumerate(ang_j_suavizado):
                ang_maximo = vAngulos_joelho_Maximos[i] if i < len(vAngulos_joelho_Maximos) else float('nan')
                print(f"Original = {angulo:.2f}, Ang Máximo: {ang_maximo:.2f}")

            #ao inves do for passa o vetor logo
            print(f"angulos originais: {ang_j_suavizado}")
            print(f"angulos maximos: {vAngulos_joelho_Maximos}")

            print(f"Angulos Tornozelo: {len(ang_t_suavizado)}, {len(vAngulos_tornozelo_Maximos)}")

            # As 3 linhas abaixo fazem o que ?
            resultados = gerar_grafico(vAngulos_joelho_Maximos, vAngulos_tornozelo_Maximos)#isso adquire os resultados.
            resultados['video'] = self.current_video_path #Adiciona ao dicionário de resultados o caminho do vídeo que foi analisado | Isso será usado no PDF para referência 
            gerar_pdf(resultados) #Chama a função gerar_grafico passando os ângulos máximos filtrados do joelho e tornozelo

            self.label_video.setText("Análise concluída!")
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