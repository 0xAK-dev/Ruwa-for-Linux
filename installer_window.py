import logging
import os
import sys

from PySide6 import QtGui
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QStackedWidget, QVBoxLayout, QWidget

from pages.installation_сomplete import InstallationComplite
from pages.lisence import LicensePage
from pages.select_version import SelectRuwaVersion
from pages.setup_options import SetupOptions
from pages.welcome_page import WelcomePage
from resources.styles import stylesheet
from widgets.page_indicator import PageIndicator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

os.environ["QT_QPA_PLATFORMTHEME"] = "xdgdesktopportal"


class Installer(QWidget):
    page_class = {
        0: WelcomePage,
        1: LicensePage,
        2: SelectRuwaVersion,
        3: SetupOptions,
        4: InstallationComplite,
    }

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ruwa Installer")
        self.setStyleSheet(
            stylesheet.widget_style + "\n" + stylesheet.label_style
        )
        
        self.setFixedSize(720, 540)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        background = QPixmap("resources/images/bg.webp").scaled(
            400, 440, Qt.IgnoreAspectRatio, Qt.SmoothTransformation
        )

        self.background_label = QLabel(self)
        self.background_label.setGeometry(self.rect())

        self.background_label.setPixmap(background)
        self.background_label.setScaledContents(True)
        self.background_label.lower()

        
        self.stack = QStackedWidget()
        self.pages = {}
        
        self.options = {}
        self.version = ""
        layout.addWidget(self.stack)
        
        self.indicator = PageIndicator(parent=self.stack, count=len(self.page_class))
        self.indicator.move(
            (self.width()-self.indicator.width()) // 2,
            480
        )
        
        self.load_page(0)
        self.indicator.raise_()

    def load_page(self, index):
        if index in self.pages:
            return self.pages[index]

        page_class = self.page_class.get(index, None)
        
        if page_class is None:
            return
            
        if page_class is InstallationComplite:
            page = page_class(self.options, self.version)
        else:
            page = page_class()
        
        self.pages[index] = page     
        self.stack.addWidget(page)
        
        if hasattr(page, "installRequested"):
            page.installRequested.connect(self.handle_install_options)

        if hasattr(page, "version_select_request"):
            page.version_select_request.connect(self.handle_version_select)
    
        if hasattr(page, "nextRequested"):
            page.nextRequested.connect(
                lambda: self.show_page(1)
            )
            
        if hasattr(page, "backRequested"):
            page.backRequested.connect(
                lambda: self.show_page(-1)
            )
          
        if hasattr(page, "closeRequested"):
            page.closeRequested.connect(self.close)

    def handle_install_options(self, options: dict):
        self.options = options

    def handle_version_select(self, version: str):
        self.version = version
        
    
    def show_page(self, step_offset):
        step = self.stack.currentIndex() + step_offset
        self.load_page(step)
        self.stack.setCurrentWidget(self.pages[step])
        self.indicator.set_step(step)
        self.indicator.raise_()

    def closeEvent(self, event):
        event.accept()

if __name__ == "__main__":
    app = QApplication()
    
    app.setWindowIcon(QtGui.QIcon('resources/images/bg.png'))
    win = Installer()
    win.show()


    sys.exit(app.exec())
