from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
)

from resources.styles import stylesheet
from widgets.button import CapsuleButton
from widgets.custom_widget import AnimateWidget


class WelcomePage(QWidget):
    nextRequested = Signal(int)
    
    def __init__(self) -> None:
        super().__init__()
        self.setFixedSize(720, 540)


        self.main_layout = QVBoxLayout(self)

        title_icon = QLabel()
        icon = QPixmap("resources/images/ruwa.svg").scaled(
            100,
            100,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        title_icon.setStyleSheet("""
            background: #131313;
            border-radius: 20px;
        """)

        title_icon.setPixmap(icon)
        title_icon.setFixedSize(100, 100)
        title_label = QLabel(text="Welcome to ruwa")

        font = QFont("Noto Sans", 30)
        title_label.setFont(font)

        label2 = QLabel(text="create without boundaries")
        label2.setStyleSheet(stylesheet.label_second_style)
        font = QFont("Arial", 11)
        font.setBold(True)
        label2.setFont(font)

        self.button = CapsuleButton(
            "Begin Installation",
            self,
            fill_color=(250, 250, 250, 220),
            text_color=(20, 20, 20, 220),
            hover_alpha=255,
            font_bold=False,
            font="Arial",
            font_size=11,
            padding_x=35,
            padding_y=12,
            animation_duration=30
        )
        self.button.clicked.connect(self.next_page)


        self.main_layout.setSpacing(10)

        self.main_layout.addStretch(2)
        self.main_layout.addWidget(title_icon, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(label2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addStretch(2)

        self.setLayout(self.main_layout)
        
    def next_page(self):
        self.nextRequested.emit(1)
   
    def showEvent(self, event) -> None:
        self.animator = AnimateWidget(self.main_layout)
        self.animator.animate_widget()
