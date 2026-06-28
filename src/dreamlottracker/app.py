from PySide6.QtWidgets import QApplication

from dreamlottracker.ui.main_window import MainWindow


class DreamLotApplication:

    def __init__(self):
        self.qt = QApplication([])
        self.window = MainWindow()

    def run(self):
        self.window.show()
        self.qt.exec()
