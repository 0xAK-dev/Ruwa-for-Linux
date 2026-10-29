from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import (
    QColor,
    QPainter,
)
from PySide6.QtWidgets import QPushButton


class PageIndicator(QPushButton):
    def __init__(
        self,
        parent=None,
        current: int = 0,
        count: int = 4
    ):
        super().__init__(parent)
        
        self.count = count
        self.active_width = 25
        self.spacing = 18
        self.current = current                         # текущая активная страница
    
        self.positions = []
        self.calculate_positions()

       
        self.next_step = 1                            # куда переключаемся
        self.animated_x = self.positions[current]   # где сейчас полоска
        self.target_x = 0

        self.setFixedSize(120, 30)

        
        self.timer = QTimer()
        self.timer.timeout.connect(self.move_animation)


    def calculate_positions(self):
        x = 0
        for _ in range(self.count):
            self.positions.append(x)
            x += self.spacing

             
    def set_step(self, step):
        self.next_step = step
        self.target_x = self.positions[step]
    
        if not self.timer.isActive():
            self.timer.start(10)
            
    def move_animation(self):
        speed = 2
        if abs(self.animated_x - self.target_x) <= speed:
            self.animated_x = self.target_x

            self.current = self.next_step
            self.timer.stop()
    
        elif self.animated_x < self.target_x:
            self.animated_x += speed
    
        else:
            self.animated_x -= speed
    
        self.update()

    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(Qt.PenStyle.NoPen)
        
        x = 0
        
        for i in range(self.count):
            
            if i == self.current:
                painter.setBrush(QColor("white"))
                painter.drawRoundedRect(self.animated_x, 0, 25, 7, 3.5, 3.5)
                x += self.active_width + self.spacing - 6         

            else:
                painter.setBrush(QColor("#262626"))
                painter.drawEllipse(x, 0, 7, 7)
                x += self.spacing
       
