from PySide6.QtWidgets import QLabel, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

from dreamlottracker.repositories.property_repository import PropertyRepository


class PropertiesPage(QWidget):
    def __init__(self):
        super().__init__()

        self.repository = PropertyRepository()

        layout = QVBoxLayout()

        title = QLabel("Properties")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")

        add_button = QPushButton("Add Property")

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            "Address",
            "City",
            "Price",
            "Acres",
            "Dream Score",
            "Status",
        ])

        layout.addWidget(title)
        layout.addWidget(add_button)
        layout.addWidget(self.table)

        self.setLayout(layout)

        self.load_properties()

    def load_properties(self):
        properties = self.repository.get_all()
        self.table.setRowCount(len(properties))

        for row, prop in enumerate(properties):
            self.table.setItem(row, 0, QTableWidgetItem(prop.address))
            self.table.setItem(row, 1, QTableWidgetItem(prop.city))
            self.table.setItem(row, 2, QTableWidgetItem(f"${prop.asking_price:,.0f}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{prop.acres:.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{prop.dream_score:.0f}"))
            self.table.setItem(row, 5, QTableWidgetItem(prop.status))
