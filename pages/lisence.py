from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QSpacerItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from resources.styles import stylesheet
from utils.lisence_text import LICENSE
from widgets.button import CapsuleButton
from widgets.checkbox import CheckBox
from widgets.custom_widget import AnimateWidget


class LicensePage(QWidget):
    backRequested = Signal(int)
    nextRequested = Signal(int)

    def __init__(self):
        super().__init__()
        self.setFixedSize(720, 540)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(5)
        self.setContentsMargins(50, 40, 50, 10)
        title_label = QLabel(text="Ruwa Lisence")

        font = QFont("Noto Sans", 25)
        title_label.setFont(font)

        label2 = QLabel(text="Please review the license terms before continuing.")
        font = QFont("Arial", 10)
        label2.setStyleSheet(stylesheet.label_second_style)
        label2.setFont(font)
        
        self.text = QTextEdit(self)
        self.text.setStyleSheet(stylesheet.text_edit_style + stylesheet.scrollbar_style)
        self.text.setReadOnly(True)
        self.text.setPlainText(LICENSE)

        self.checkbox = CheckBox(
            text="I have read and accept the Ruwa lisense terms", radius=5
        )
        self.checkbox.checkStateChanged.connect(self.accept_lisense)

        self.continue_btn = CapsuleButton(
            text="Continue",
            font_bold=False,
            padding_x=35,
            padding_y=12,
            fill_color=(250, 250, 250, 220),
            text_color=(20, 20, 20, 230),
            animation_duration=30,
            font_size=11,
            font="Arial",
        )

        self.continue_btn.setDisabled(True)
        self.continue_btn.clicked.connect(self.next_page)

        self.previous_btn = CapsuleButton(
            text=" Back",
            radius=7,
            padding_x=6,
            padding_y=2,
            text_color=(200, 200, 200, 140),
            fill_color=(35, 35, 35),
            animation_duration=100,
        )
        self.previous_btn.clicked.connect(self.go_back)

        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.previous_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        nav_layout.addWidget(self.continue_btn, alignment=Qt.AlignmentFlag.AlignRight)

        self.main_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addWidget(label2, alignment=Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addItem(
            QSpacerItem(0, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        )
        self.main_layout.addWidget(self.text, stretch=1)
        self.main_layout.addItem(
            QSpacerItem(0, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        )
        self.main_layout.addWidget(self.checkbox)
        self.main_layout.addItem(
            QSpacerItem(0, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        )
        self.main_layout.addLayout(nav_layout)
        self.main_layout.addItem(
            QSpacerItem(0, 50, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        )

        self.setLayout(self.main_layout)

    def go_back(self):
        self.backRequested.emit(-1)

    def next_page(self):
        self.nextRequested.emit(1)

    def accept_lisense(self):
        self.continue_btn.setDisabled(not self.checkbox.isChecked())

    def showEvent(self, event) -> None:
        self.animator = AnimateWidget(self.main_layout)
        self.animator.animate_widget()
