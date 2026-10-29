from pathlib import Path, PurePosixPath

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QFileDialog, QLineEdit

from widgets.button import CapsuleButton


class PathSelector(QLineEdit):
    def __init__(
        self,
        path: PurePosixPath | str,
        height: int = 50,
        focus_border_color=(150, 150, 150),
        border_color=(50, 50, 50),
        fill_color=(0, 0, 0, 0),
        border_width: int = 1,
        radius: int | None = None,
        font="JetBrainsMono",
        font_bold=False,
    ):
        super().__init__()

        self._path = path
        self.setText(str(path))

        self.setFixedHeight(height)

        font = QFont(font, self.height() // 4)
        font.setBold(font_bold)
        self.setFont(font)

        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.textEdited.connect(self.set_custom_path)

        def color_to_qss(color):
            if isinstance(color, tuple):
                if len(color) == 3:
                    return f"rgb({color[0]}, {color[1]}, {color[2]})"
                elif len(color) == 4:
                    return f"rgba({color[0]}, {color[1]}, {color[2]}, {color[3]})"

            return color

        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: {color_to_qss(fill_color)};
                color: white;
                border: {border_width}px solid {color_to_qss(border_color)};
                border-radius: {radius if radius is not None else self.height() // 2}px;
                padding: 12px 20px;
            }}

            
            QLineEdit:focus {{
                border: 2px solid {color_to_qss(focus_border_color)};
            }}
            
            QLineEdit:disabled {{
                background-color: #222222;
                color: #777777;
            }}
        """)

        self.button = CapsuleButton(
            "Change",
            self,
            radius=0,
            padding_x=20,
            text_color=(200, 200, 200, 140),
            fill_color=(26, 26, 26),
            animation_duration=100,
        )
        self.button.setFixedHeight(self.height() - border_width * 2)
        self.button.move(self.width() - self.button.width() - 60, 1)
        self.button.clicked.connect(self.set_installation_path)

    def set_installation_path(self):
        dialog = QFileDialog()

        directory = dialog.getExistingDirectory(
            self, "Выберите папку", str(Path.home())
        )

        if directory:
            self.setText(directory)
            self.path = directory


    def set_custom_path(self, text):
        self.path = text


    @property
    def path(self) -> Path:
        return self._path

    @path.setter
    def path(self, path: PurePosixPath | str):
        self._path = Path(path).expanduser()

