from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from resources.styles import stylesheet
from widgets.button import CapsuleButton
from widgets.checkbox import CheckBox
from widgets.custom_widget import AnimateWidget
from widgets.path_selector import PathSelector


class SetupOptions(QWidget):
    installRequested = Signal(dict)
    backRequested = Signal(int)
    nextRequested = Signal(int)

    def __init__(self):
        super().__init__()
        self.setFixedSize(720, 540)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(12)
        self.setContentsMargins(50, 40, 50, 10)
        title_label = QLabel(text="Setup options")

        font = QFont("Noto Sans", 25)
        title_label.setFont(font)

        label2 = QLabel(text="Choose where to install and what to include.")
        font = QFont("Arial", 10)
        label2.setStyleSheet(stylesheet.label_second_style)
        label2.setFont(font)

        label3 = QLabel(text="INSTALL LOCATION")
        font = QFont("Arial", 10)
        label3.setStyleSheet(stylesheet.label_second_style)
        label3.setFont(font)

        label4 = QLabel(text="Option")
        font = QFont("Arial", 10)
        label4.setStyleSheet(stylesheet.label_second_style)
        label4.setFont(font)

        self.path_selector = PathSelector(path="~/.local/bin/ruwa", font="Arial")
        self.checkbox1 = CheckBox(text="Create desktop shortcut", radius=5)
        self.checkbox1.setChecked(True)
        self.checkbox1.clicked.connect(self.hide_options)
        self.checkbox2 = CheckBox(
            text="Force Qt to use X11 instead of Wayland (QT_QPA_PLATFORM=xcb)",
            radius=5,
        )
        self.checkbox3 = CheckBox(
            text="Use xdg-desktop-portal (QT_QPA_PLATFORMTHEME=xdgdesktopportal)",
            radius=5,
        )
        self.checkbox4 = CheckBox(
            text="Force NVIDIA driver selection for OpenGL (__GLX_VENDOR_LIBRARY_NAME=nvidia)",
            radius=5,
        )
        self.checkbox5 = CheckBox(
            text="Disable BUILD_TESTING (-DBUILD_TESTING=OFF)",
            radius=5,
        )

        self.continue_btn = CapsuleButton(
            text="Continue",
            font_bold=False,
            padding_x=35,
            padding_y=12,
            fill_color=(250, 250, 250, 220),
            text_color=(20, 20, 20, 220),
            animation_duration=30,
            font_size=11,
            font="Arial",
        )
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
        self.main_layout.addWidget(label3)
        self.main_layout.addWidget(self.path_selector)
        self.main_layout.addWidget(label4)
        self.main_layout.addWidget(self.checkbox1)
        self.main_layout.addWidget(self.checkbox2)
        self.main_layout.addWidget(self.checkbox3)
        self.main_layout.addWidget(self.checkbox4)
        self.main_layout.addWidget(self.checkbox5)
        self.main_layout.addStretch()
        self.main_layout.addLayout(nav_layout)

        self.main_layout.addItem(
            QSpacerItem(0, 50, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        )

        self.setLayout(self.main_layout)

    def go_back(self):
        self.backRequested.emit(-1)

    def next_page(self):
        options = self.get_install_options()
        self.installRequested.emit(options)
        self.nextRequested.emit(1)

    def get_install_options(self):
        options = {
            "add_shortcut": self.checkbox1.isChecked(),
        }
        options["path"] = self.path_selector.path

        if self.checkbox2.isChecked():
            options["QT_QPA_PLATFORM"] = "xcb"

        if self.checkbox3.isChecked():
            options["QT_QPA_PLATFORMTHEME"] = "xdgdesktopportal"

        if self.checkbox4.isChecked():
            options["__GLX_VENDOR_LIBRARY_NAME"] = "nvidia"

        if self.checkbox5.isChecked():
            options["-DBUILD_TESTING"] = "OFF"

        return options

    def hide_options(self):
        visible = self.checkbox1.isChecked()

        self.checkbox2.setVisible(visible)
        self.checkbox3.setVisible(visible)
        self.checkbox4.setVisible(visible)

        if not visible:
            self.checkbox2.setChecked(False)
            self.checkbox3.setChecked(False)
            self.checkbox4.setChecked(False)

    def showEvent(self, event) -> None:
        self.animator = AnimateWidget(self.main_layout)
        self.animator.animate_widget()
