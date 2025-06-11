from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

def open_history_window():
    dialog = QDialog()
    dialog.setWindowTitle("Histórico de Análises")
    dialog.setMinimumSize(300, 200)

    layout = QVBoxLayout()

    label = QLabel("Histórico de análises ainda não implementado.\nEm breve, você poderá ver gráficos antigos aqui.")
    layout.addWidget(label)

    btn_close = QPushButton("Fechar")
    btn_close.clicked.connect(dialog.accept)
    layout.addWidget(btn_close)

    dialog.setLayout(layout)
    dialog.exec()



# gui/history.py

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

def show_history_plot(data):  # <- ESSA FUNÇÃO PRECISA EXISTIR
    dialog = QDialog()
    dialog.setWindowTitle("Histórico de Ângulos")
    dialog.resize(600, 400)

    layout = QVBoxLayout(dialog)
    canvas = PlotCanvas(data)
    layout.addWidget(canvas)

    dialog.setLayout(layout)
    dialog.exec()

class PlotCanvas(FigureCanvas):
    def __init__(self, data, parent=None):
        fig = Figure(figsize=(5, 4))
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.plot(data)

    def plot(self, data):
        self.axes.clear()
        self.axes.plot(data, label="Ângulo estimado")
        self.axes.set_title("Evolução dos Ângulos")
        self.axes.set_xlabel("Frame")
        self.axes.set_ylabel("Ângulo (°)")
        self.axes.legend()
        self.draw()
