import sys

from PySide6.QtCore import QPointF, QRectF, Qt, QTimer
from PySide6.QtGui import QColor, QFont, QPainter, QPainterPath, QPen

from PySide6.QtWidgets import QCheckBox

class CheckBox(QCheckBox):
    def __init__(
        self,
        text,
        parent=None,
        box_size=20,
        border_width=1,
        text_color=(0, 0, 0),
        normal_alpha: int = 170,
        hover_alpha: int = 255,
        border_color=(50, 50, 50),
        fill_color=(60, 60, 60),
        radius: int | None = None,
        font="JetBrainsMono",
        font_bold=True,
    ):
        super().__init__(text, parent)

        self.box_size = box_size
        self.text_color = text_color
        self.border_color = border_color
        self.fill_color = fill_color
        self.radius = radius
        self.border_width = border_width

        font = QFont(font, 10)
        font.setBold(font_bold)
        self.setFont(font)

        self.setCursor(Qt.PointingHandCursor)

        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_text)

        self.alpha = normal_alpha  # текущее значение
        self.target_alpha = normal_alpha  # цель анимации

        self.normal_alpha = normal_alpha  # обычное состояние
        self.hover_alpha = hover_alpha  # при наведении

    def enterEvent(self, event):
        self.target_alpha = self.hover_alpha
        self.timer.start(4)

    def leaveEvent(self, event):
        self.target_alpha = self.normal_alpha
        self.timer.start(4)

    def animate_text(self):
        if self.alpha < self.target_alpha:
            self.alpha = min(self.alpha + 5, self.target_alpha)

        elif self.alpha > self.target_alpha:
            self.alpha = max(self.alpha - 5, self.target_alpha)
        else:
            self.timer.stop()

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)  # Сглаживание
        margin = 6
        box_rect = QRectF(
            margin,
            (self.height() - self.box_size) / 2,
            self.box_size,
            self.box_size,
        )

        radius = self.radius if self.radius is not None else 6

        path = QPainterPath()
        path.addRoundedRect(box_rect, radius, radius)

        painter.setClipping(False)

        if self.isChecked():
            painter.fillPath(path, QColor(255, 255, 255))
            
        pen = QPen(QColor(255, 255, 255, self.alpha), self.border_width)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawRoundedRect(box_rect, radius, radius)

        if self.isChecked():
            pen = QPen(QColor(0, 0, 0, self.alpha), 2)
            pen.setCapStyle(Qt.RoundCap)
            pen.setJoinStyle(Qt.RoundJoin)
            painter.setPen(pen)

            x = box_rect.x()
            y = box_rect.y()

            s = box_rect.width()

            painter.drawLine(
                QPointF(x + s * 0.25, y + s * 0.55),
                QPointF(x + s * 0.45, y + s * 0.75),
            )

            painter.drawLine(
                QPointF(x + s * 0.45, y + s * 0.75),
                QPointF(x + s * 0.75, y + s * 0.30),
            )
            

        painter.setPen(QColor(255, 255, 255, self.alpha))
        
        text_rect = QRectF(
            box_rect.right() + 10,
            0,
            self.width() - box_rect.width() - 16,
            self.height(),
        )

        painter.drawText(text_rect, Qt.AlignVCenter | Qt.AlignLeft, self.text())
