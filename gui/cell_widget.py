from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import Qt

class CellWidget(QWidget):
    def __init__(self, row, col, click_callback):
        super().__init__()
        self.row = row
        self.col = col
        self.alive = False
        self.click_callback = click_callback
        self.setFixedSize(25, 25)
        self.update_color()

    def mousePressEvent(self, event):
        self.alive = not self.alive
        self.update_color()
        self.click_callback(self.row, self.col, self.alive)

    def update_color(self):
        color = QColor("#4CAF50") if self.alive else QColor("#DDDDDD")
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, color)
        self.setAutoFillBackground(True)
        self.setPalette(palette)
