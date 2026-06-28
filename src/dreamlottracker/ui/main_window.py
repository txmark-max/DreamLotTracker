from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from dreamlottracker.version import APP_NAME, VERSION


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_NAME)
        self.resize(1000, 700)

        widget = QWidget()

        layout = QVBoxLayout()

        title = QLabel(APP_NAME)
        title.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
        """)

        version = QLabel(VERSION)

        status = QLabel("✅ Database Connected")

        welcome = QLabel("Welcome, Mark!")

        layout.addWidget(title)
        layout.addWidget(version)
        layout.addSpacing(20)
        layout.addWidget(status)
        layout.addSpacing(20)
        layout.addWidget(welcome)
        layout.addStretch()

        widget.setLayout(layout)

        self.setCentralWidget(widget)
