from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QWidget

class LoadingWidget(QWidget):
    def __init__(
        self,
        line_width=10,
        color=(255, 255, 255),
        size: int = 80
    ):
        super().__init__()
        self.setFixedSize(size, size)
        self.angle = 0
        self.color = color
        self.line_width = line_width
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)
        self.timer.start(40)  # ~20 FPS

    def rotate(self):
        self.angle = (self.angle + 10) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
        pen = QPen(QColor(*self.color), self.line_width)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
    
        rect = self.rect().adjusted(10, 10, -10, -10)
    
        painter.drawArc(
            rect,
            self.angle * 16,      # начало
            120 * 16              # длина дуги
        )