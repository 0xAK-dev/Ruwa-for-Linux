import logging

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import (
    QLabel,
    QProgressBar,
    QSizePolicy,
    QSpacerItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from core.installer import RuwaInstaller
from resources.styles import stylesheet
from utils.exceptions import UnsupportedDistributionError
from widget.button import CapsuleButton
from widget.custom_widget import AnimateWidget
from widget.loading_widget import LoadingWidget

logger = logging.getLogger(__name__)


class WorkerThread(QThread):
    status = Signal(str)
    failed = Signal(str)
    finished = Signal(str)

    def __init__(self, options: dict, version: str):
        super().__init__()
        self.options = options
        self.version = version
        
        self.path = options.pop("path")
        self.add_shortcut = options.pop("add_shortcut")

    def run(self):
        logger.info("Starting installer")

        installer = RuwaInstaller(
            options=self.options, version=self.version, path=self.path
        )

        self.status.emit("Checking dependencies...")
        try:
            missing_pkg = installer.check_packages()
        except UnsupportedDistributionError as e:
            self.failed.emit(str(e))
            return
            
        if missing_pkg:
            distro, like = installer.get_distro_and_like()
            self.failed.emit(
                f"Missing dependencies: {' '.join(missing_pkg)}\n"
                f"To install them, run:\n"
                f"sudo {''.join(installer.get_package_install_command(distro, like))} {' '.join(missing_pkg)}"
            )
            return

        self.status.emit("Downloading Ruwa source code...")
        if (error := installer.download_ruwa()) is not None:
            self.failed.emit(f"Failed to download Ruwa: {error}")
            return

        self.status.emit("Applying patches and configuring CMake...")
        if (error := installer.configure()) is not None:
            self.failed.emit(f"CMake configuration failed:\n{error}")
            return

        self.status.emit("Building project (this may take 1–5 minutes)...")
        if (build_result := installer.build()) is not None:
            if "FAILED: [code=1] tests/RuwaTests" in build_result:
                logger.error("RuwaTests build failed. Try CMake flag -DBUILD_TESTING=OFF.")
                msg = "Test build failed (RuwaTests). Try disabling tests using -DBUILD_TESTING=OFF."
                self.failed.emit(f"Build failed:\n{msg}\n\n{build_result}")
            else:
                self.failed.emit(f"Build failed:\n{build_result}")
            return

        self.status.emit(f"Installing files to {self.path}")
        install_result = installer.install()
        if install_result is not None:
            self.failed.emit(f"Installation failed:\n{install_result}")
            return
            
        if self.add_shortcut:
            self.status.emit("Creating shortcut...")
            installer.create_shortcut()

        self.finished.emit("Installation completed successfully")


class InstallationComplite(QWidget):
    closeRequested = Signal()

    def __init__(self, options: dict, version: str):
        super().__init__()
        self.options = options
        self.version = version
        self.setFixedSize(720, 540)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(5)
        self.setContentsMargins(50, 40, 50, 10)

        self.success_widget = QLabel()
        self.success_widget.setFixedSize(80, 80)
        self.success_widget.setPixmap(QPixmap("resources/images/success.svg"))
        self.success_widget.setScaledContents(True)
        self.success_widget.hide()

        self.loading_widget = LoadingWidget()
        label1 = QLabel(text=f"Installing Ruwa {self.version}")
        font = QFont("Noto Sans", 30)
        label1.setFont(font)

        label2 = QLabel(text="The will only take a moment.")
        label2.setStyleSheet(stylesheet.label_second_style)
        font = QFont("Arial", 11)
        font.setBold(True)
        label2.setFont(font)

        self.progres_bar = QProgressBar(self)
        self.progres_bar.setStyleSheet(stylesheet.progress_bar_style + stylesheet.scrollbar_style)
        self.progres_bar.setRange(0, 6)
        self.progres_bar.setTextVisible(False)
        self.progres_bar.setValue(0)

        self.status_text = QLabel(text="Status")
        font = QFont("Arial", 11)
        self.status_text.setFont(font)

        self.close_btn = CapsuleButton(
            text="Close",
            font_bold=False,
            padding_x=35,
            padding_y=12,
            fill_color=(250, 250, 250, 220),
            text_color=(20, 20, 20, 220),
            animation_duration=30,
            font_size=11,
            font="Arial",
        )
        self.close_btn.hide()
        self.close_btn.clicked.connect(self.closeRequested.emit)

        self.main_layout.setSpacing(10)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(
            self.success_widget, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.main_layout.addWidget(
            self.loading_widget, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.main_layout.addWidget(label1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(label2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addItem(
            QSpacerItem(0, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        )

        self.main_layout.addWidget(self.progres_bar)
        self.main_layout.addWidget(self.status_text)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(
            self.close_btn, alignment=Qt.AlignmentFlag.AlignRight
        )
        self.main_layout.addStretch(2)

        self.setLayout(self.main_layout)

    def start_instalation(self):
        self.installer = WorkerThread(options=self.options, version=self.version)

        self.installer.status.connect(self.handle_install_status)
        self.installer.failed.connect(self.handle_install_failed)
        self.installer.finished.connect(self.handle_install_finished)

        self.installer.start()

    def handle_install_status(self, status_text):
        logger.info(status_text)
        self.status_text.setStyleSheet(stylesheet.label_second_style)
        self.status_text.setText(status_text)
        self.progres_bar.setValue(self.progres_bar.value() + 1)

    def handle_install_failed(self, error_text):
        self.loading_widget.hide()
        logger.error(error_text)

        label = self.status_text

        self.error_text = QTextEdit(self)
        self.error_text.setStyleSheet(stylesheet.text_edit_error_style)
        self.error_text.setFixedHeight(100)
        self.error_text.setReadOnly(True)
        self.error_text.setPlainText(error_text)

        self.main_layout.replaceWidget(label, self.error_text)

        label.hide()
        self.close_btn.show()

    def handle_install_finished(self, finished_text):
        self.loading_widget.hide()
        self.success_widget.show()
        self.status_text.setStyleSheet(stylesheet.label_success_style)
        self.status_text.setText(finished_text)
        self.progres_bar.setValue(self.progres_bar.value() + 1)
        self.close_btn.show()

    def showEvent(self, event) -> None:
        self.animator = AnimateWidget(self.main_layout)
        self.animator.animate_widget()
        self.start_instalation()
