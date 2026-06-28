from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class PlaceholderPage(QWidget):
    def __init__(self, title: str):
        super().__init__()

        layout = QVBoxLayout()

        heading = QLabel(title)
        heading.setStyleSheet("font-size: 24px; font-weight: bold;")

        note = QLabel("This section will be built in a future sprint.")
        note.setStyleSheet("font-size: 14px; color: gray;")

        layout.addWidget(heading)
        layout.addWidget(note)
        layout.addStretch()

        self.setLayout(layout)
