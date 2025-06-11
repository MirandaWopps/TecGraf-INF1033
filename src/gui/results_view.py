from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton
from PySide6.QtGui import QPixmap
import os

def show_results():
    dialog = QDialog()
    dialog.setWindowTitle("Resultados da Análise")
    dialog.setMinimumSize(600, 400)

    layout = QVBoxLayout()

    label = QLabel("Gráfico gerado:")
    layout.addWidget(label)

    image_path = os.path.join("data", "ultimo_grafico.png")
    if os.path.exists(image_path):
        pixmap = QPixmap(image_path)
        img_label = QLabel()
        img_label.setPixmap(pixmap.scaled(560, 300))
        layout.addWidget(img_label)
    else:
        layout.addWidget(QLabel("Nenhum gráfico encontrado."))

    btn_close = QPushButton("Fechar")
    btn_close.clicked.connect(dialog.accept)
    layout.addWidget(btn_close)

    dialog.setLayout(layout)
    dialog.exec()
