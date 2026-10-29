from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QAbstractItemView, QFrame, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget

from config import VERSIONS
from resources.styles.stylesheet import list_widget, scrollbar_style
from widgets.button import CapsuleButton
from widgets.custom_widget import AnimateWidget

class SelectRuwaVersion(QWidget):
    version_select_request = Signal(str)
    backRequested = Signal(int)
    nextRequested = Signal(int)
    
    def __init__(self):
        super().__init__()

        self.version = None
        
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(17)
        
        label = QLabel(text="Select Ruwa version")
        font = QFont("Noto Sans", 25)
        label.setFont(font)
        self.setContentsMargins(50, 40, 50, 10)
        
        self.version_widget = QListWidget(self)
        self.version_widget.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.version_widget.setStyleSheet(list_widget + scrollbar_style)
        for version in VERSIONS:
           self.add_version_item(version)
           
        self.version_widget.setFixedSize(420, 300)
        self.version_widget.setCurrentRow(0)
        self.version_widget.itemSelectionChanged.connect(self.change_selection)


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
        

        self.main_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.version_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addLayout(nav_layout)
        self.main_layout.addStretch()
        self.setLayout(self.main_layout)
        
        self.change_selection()

    def go_back(self):
        self.backRequested.emit(-1)

    def next_page(self):
        self.version_select_request.emit(self.version)
        self.nextRequested.emit(1)

    def add_version_item(self, version):
        item = QListWidgetItem()
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 0, 5, 0)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFixedWidth(4)
        line.setStyleSheet("background-color: white; border-radius: 2px;")

        version = QLabel(version)
        check = QLabel("")
        
        layout.addWidget(line)
        layout.addWidget(version)
        layout.addStretch()
        layout.addWidget(check)

        item.setData(Qt.UserRole, version)
        item.setData(Qt.UserRole + 1, check)
        item.setData(Qt.UserRole + 2, line)
        self.version_widget.addItem(item)
        self.version_widget.setItemWidget(item, widget)
        

    def change_selection(self):
        for i in range(0, self.version_widget.count()):
            item = self.version_widget.item(i)
            check = item.data(Qt.UserRole + 1)
            line = item.data(Qt.UserRole + 2) 
            if item.isSelected():
                self.version = item.data(Qt.UserRole).text()
                check.setText("")
                line.show()
            else:
                check.setText("")
                line.hide()

    def showEvent(self, event) -> None:
        self.animator = AnimateWidget(self.main_layout)
        self.animator.animate_widget()
    
