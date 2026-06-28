from PySide6.QtWidgets import QLabel, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget


class PropertiesPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("Properties")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")

        add_button = QPushButton("Add Property")

        table = QTableWidget(0, 6)
        table.setHorizontalHeaderLabels([
            "Address",
            "City",
            "Price",
            "Acres",
            "Dream Score",
            "Status",
        ])

        layout.addWidget(title)
        layout.addWidget(add_button)
        layout.addWidget(table)

        self.setLayout(layout)
