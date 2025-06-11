import sys  # Importa o módulo sys para manipulação do sistema e argumentos da linha de comando
from PySide6.QtWidgets import (  # Importa widgets do PySide6 para criar a interface gráfica
    QApplication, QMainWindow, QPushButton, QVBoxLayout,
    QWidget, QFileDialog, QLabel, QHBoxLayout, QMessageBox 
)
from PySide6.QtGui import QIcon  # Importa QIcon para ícones na interface (não utilizado aqui)
from PySide6.QtCore import Qt    # Importa constantes e funcionalidades do Qt

from analysis.analysis import analyze_video, analyze_webcam  # Importa funções de análise de vídeo e webcam
from .history import open_history_window  # Importa função para abrir a janela de histórico

class MainWindow(QMainWindow):  # Define a classe principal da janela, herdando de QMainWindow
    def __init__(self):  # Método construtor da janela principal
        super().__init__()  # Inicializa a classe base QMainWindow
        self.setWindowTitle("Análise de Movimento") # Define o título da janela
        self.setGeometry(100, 100, 400, 300) # Define a posição e tamanho da janela

        # Layout principal
        layout = QVBoxLayout()  # Cria um layout vertical para organizar os widgets
        layout.setAlignment(Qt.AlignCenter)  # Centraliza os widgets no layout

        self.label = QLabel("Selecione uma opção")  # Cria um label com texto inicial
        self.label.setAlignment(Qt.AlignCenter)     # Centraliza o texto do label
        layout.addWidget(self.label)                # Adiciona o label ao layout

        # Botões principais
        btn_video = QPushButton("📹 Analisar Vídeo")  # Cria botão para analisar vídeo
        btn_video.clicked.connect(self.load_video)    # Conecta o clique do botão ao método load_video
        layout.addWidget(btn_video)                   # Adiciona o botão ao layout

        btn_webcam = QPushButton("🎥 Analisar Webcam") # Cria botão para analisar webcam
        btn_webcam.clicked.connect(self.analyze_webcam) # Conecta o clique ao método analyze_webcam
        layout.addWidget(btn_webcam)                    # Adiciona o botão ao layout

        btn_history = QPushButton("📊 Ver Histórico")   # Cria botão para ver histórico
        btn_history.clicked.connect(self.view_history)  # Conecta o clique ao método view_history
        layout.addWidget(btn_history)                   # Adiciona o botão ao layout

        btn_exit = QPushButton("🔚 Sair")               # Cria botão para sair do programa
        btn_exit.clicked.connect(self.close)            # Conecta o clique ao método close (fecha a janela)
        layout.addWidget(btn_exit)                      # Adiciona o botão ao layout

        # Centraliza os elementos
        container = QWidget()           # Cria um widget container para o layout
        container.setLayout(layout)     # Define o layout do container
        self.setCentralWidget(container) # Define o container como widget central da janela

    def load_video(self):  # Método para carregar e analisar um vídeo
        file_dialog = QFileDialog(self)  # Cria um diálogo para seleção de arquivo
        file_path, _ = file_dialog.getOpenFileName(  # Abre o diálogo e obtém o caminho do arquivo selecionado
            self, "Selecionar vídeo", "", "Videos (*.mp4 *.avi *.mov)"
        )
        if file_path:  # Se um arquivo foi selecionado
            analyze_video(file_path)  # Chama a função de análise de vídeo
            show_results()            # Exibe os resultados (função não definida neste trecho)

    def analyze_webcam(self):  # Método para analisar a webcam
        analyze_webcam()  # Chama a função de análise da webcam
        show_results()    # Exibe os resultados (função não definida neste trecho)

    def view_history(self):  # Método para abrir a janela de histórico
        open_history_window()  # Chama a função para abrir a janela de histórico
        

if __name__ == "__main__":  # Se o arquivo for executado diretamente
    app = QApplication(sys.argv)  # Cria a aplicação Qt
    window = MainWindow()         # Instancia a janela principal
    window.show()                 # Exibe a janela
    sys.exit(app.exec())          # Executa o loop principal da aplicação e encerra ao fechar