from PySide6.QtCore import QRectF, Qt, QTimer
from PySide6.QtGui import (
    QColor,
    QFont,
    QPainter,
    QPainterPath,
    QPen,
)
from PySide6.QtWidgets import QGraphicsDropShadowEffect, QPushButton


class CapsuleButton(QPushButton):
    """
        Custom capsule-shaped button with support for:
        - smooth opacity transition on hover;
        - custom text, background, and border colors;
        - rounded corners;
        - adjustable size using padding;
        - optional drop shadow;
        - RGB and RGBA color formats.
    
        Colors can be specified as:
    
            RGB:
                (255, 255, 255)
    
            RGBA:
                (255, 255, 255, 100)
    
        When using RGBA colors, the alpha channel is combined
        with the button's current opacity.
    """
    def __init__(
        self,
        text,
        parent=None,
        padding_x=20,
        padding_y=12,
        text_color=(14, 14, 14),
        hover_alpha: int = 255,
        border_color=(30, 30, 30),
        fill_color=(39, 194, 245),
        border_width: int | float | None = None,
        radius: int | None = None,
        font="JetBrainsMono",
        font_size: int = 10,
        font_bold=True,
        shadow_on = False,
        shadow_color=(205, 205, 205),
        animation_duration=400
    ):
        super().__init__(text, parent)
        self.adjustSize()
        
        self.text_color = text_color
        self.border_color = border_color
        self.fill_color = fill_color
        self.shadow_color=shadow_color
   
        self.border_width = border_width
        self.shadow_on = shadow_on
        self.radius = radius
        self.animation_duration = animation_duration

        font = QFont(font, font_size)
        font.setBold(font_bold)
        self.setFont(font)

        self.setStyleSheet(f"padding: {padding_y}px {padding_x}px;")

        self.setCursor(Qt.PointingHandCursor)

        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)

        self.alpha = 0                         # текущее значение
        self.target_alpha = 0                  # цель анимации
        self.hover_alpha = hover_alpha         # при наведении
        
        if self.shadow_on:
            self.shadow_effect = QGraphicsDropShadowEffect(self)
        
            self.shadow_effect.setColor(QColor(205, 205, 205, 0))
            self.shadow_effect.setOffset(0, 0)
            self.shadow_effect.setBlurRadius(37)
            self.setGraphicsEffect(self.shadow_effect)

    def rgba(self, color: tuple):
        if len(color) == 4:
            alpha = min(color[3] + int(self.alpha), 255)
        else:
            alpha = int(self.alpha)
    
        return QColor(
            color[0],
            color[1],
            color[2],
            alpha
        )


    def enterEvent(self, event):
        self.target_alpha = self.hover_alpha
        self.timer.start(8)
    
    def leaveEvent(self, event):
        self.target_alpha = 0
        self.timer.start(8)

    def animate(self):
        interval = 8
        steps = self.animation_duration / interval
    
        step = int(max(
            abs(self.target_alpha - self.alpha) / steps,
            1
        ))
    
        if self.alpha < self.target_alpha:
            self.alpha = int(
                min(self.alpha + step, self.target_alpha)
            )
    
        elif self.alpha > self.target_alpha:
            self.alpha = int(
                max(self.alpha - step, self.target_alpha)
            )
    
        else:
            self.timer.stop()
    
        if self.shadow_on:
            self.shadow_effect.setColor(
                self.rgba(self.shadow_color)
            )
    
        self.update()


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)  # Сглаживание

        path = QPainterPath()
        radius = self.height() / 2
        
        if self.radius is not None:
            radius = self.radius

        path.addRoundedRect(
            self.rect(), radius, radius
        )

        painter.setClipPath(path)                           # ограничиваем область рисования
        if not self.isEnabled():
            alpha = 160   # прозрачность отключенной кнопки
            fill = QColor(80, 80, 80, alpha)
            text = QColor(200, 200, 200, alpha)
            border = QColor(150, 150, 150, 0)
        else:
            fill = self.rgba(self.fill_color)
            text = self.rgba(self.text_color)
            border = self.rgba(self.border_color)


        painter.fillRect(
            self.rect(),
            fill
        )
       
        # Border
        if self.border_width is not None:
            border_rect = QRectF(self.rect()).adjusted(
                0.5,
                0.5,
                -0.5,
                -0.5,
            ) 
            pen = QPen(border, self.border_width)
            pen.setCosmetic(True)
            
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            
            painter.drawRoundedRect(
                border_rect,
                radius - 1,
                radius - 1
            )
        # Text
        painter.setPen(text)
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())

