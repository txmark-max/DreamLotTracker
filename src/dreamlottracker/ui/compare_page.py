from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from dreamlottracker.services.comparison_service import ComparisonService


class ComparePage(QWidget):
    def __init__(self):
        super().__init__()

        self.service = ComparisonService()
        self.properties = []

        layout = QVBoxLayout()

        title = QLabel("Compare Properties")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")

        subtitle = QLabel("Select two or more properties to compare side by side.")
        subtitle.setStyleSheet("font-size: 14px; color: gray;")

        content_layout = QHBoxLayout()

        left_layout = QVBoxLayout()

        self.property_list = QListWidget()
        self.property_list.setSelectionMode(QListWidget.MultiSelection)

        compare_button = QPushButton("Compare Selected")
        compare_button.clicked.connect(self.compare_selected)

        refresh_button = QPushButton("Refresh List")
        refresh_button.clicked.connect(self.load_properties)

        left_layout.addWidget(QLabel("Properties"))
        left_layout.addWidget(self.property_list)
        left_layout.addWidget(compare_button)
        left_layout.addWidget(refresh_button)

        self.comparison_table = QTableWidget()

        content_layout.addLayout(left_layout, 1)
        content_layout.addWidget(self.comparison_table, 3)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(12)
        layout.addLayout(content_layout)

        self.setLayout(layout)

        self.load_properties()

    def load_properties(self):
        self.property_list.clear()
        self.properties = self.service.get_properties()

        for property_ in self.properties:
            listing = property_.listings[0] if property_.listings else None
            scores = property_.scores

            price = listing.asking_price if listing else 0
            score = scores.dream_score if scores and scores.dream_score is not None else 0

            item = QListWidgetItem(
                f"{property_.address} — {property_.city} — ${price:,.0f} — Score {score:.1f}"
            )
            item.setData(1000, property_.id)
            self.property_list.addItem(item)

    def compare_selected(self):
        selected_items = self.property_list.selectedItems()

        if len(selected_items) < 2:
            QMessageBox.information(
                self,
                "Select Properties",
                "Please select at least two properties to compare.",
            )
            return

        selected_ids = {item.data(1000) for item in selected_items}
        selected_properties = [
            property_ for property_ in self.properties if property_.id in selected_ids
        ]

        self.populate_comparison(selected_properties)

    def populate_comparison(self, selected_properties):
        rows = self.service.build_comparison_rows(selected_properties)

        self.comparison_table.clear()
        self.comparison_table.setRowCount(len(rows))
        self.comparison_table.setColumnCount(len(selected_properties) + 1)

        headers = ["Metric"] + [property_.address for property_ in selected_properties]
        self.comparison_table.setHorizontalHeaderLabels(headers)

        for row_index, (metric, values) in enumerate(rows):
            self.comparison_table.setItem(row_index, 0, QTableWidgetItem(metric))

            for col_index, value in enumerate(values, start=1):
                self.comparison_table.setItem(row_index, col_index, QTableWidgetItem(value))

        self.comparison_table.resizeColumnsToContents()
