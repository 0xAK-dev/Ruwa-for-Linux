from PySide6.QtCore import QPropertyAnimation, QTimer
from PySide6.QtWidgets import QGraphicsOpacityEffect


class AnimateWidget:
    def __init__(self, layout):
        self.layout = layout
        self.animations = []
        self.effects = []

    def animate_widget(self):
        for i in range(self.layout.count()):
            item = self.layout.itemAt(i)
            widget = item.widget()

            if not widget:
                continue

            effect = QGraphicsOpacityEffect(widget)
            effect.setOpacity(0)

            widget.setGraphicsEffect(effect)

            self.effects.append(effect)

            animation = QPropertyAnimation(effect, b"opacity")
            animation.setDuration(100)
            animation.setStartValue(0)
            animation.setEndValue(1)

            QTimer.singleShot(
                i * 50,
                animation.start
            )

            self.animations.append(animation)