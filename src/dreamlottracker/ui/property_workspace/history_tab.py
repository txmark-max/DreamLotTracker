from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget


class HistoryTab(QWidget):
    def __init__(self, property_):
        super().__init__()

        layout = QVBoxLayout()

        listing = property_.listings[0] if property_.listings else None
        history = listing.price_history if listing else []
        history = sorted(history, key=lambda item: item.recorded_date, reverse=True)

        table = QTableWidget(len(history), 3)
        table.setHorizontalHeaderLabels(["Date", "Price", "Note"])

        for row, entry in enumerate(history):
            table.setItem(row, 0, QTableWidgetItem(entry.recorded_date.strftime("%Y-%m-%d")))
            table.setItem(row, 1, QTableWidgetItem(f"${entry.price:,.0f}"))
            table.setItem(row, 2, QTableWidgetItem(entry.note or ""))

        table.resizeColumnsToContents()
        layout.addWidget(table)
        self.setLayout(layout)
