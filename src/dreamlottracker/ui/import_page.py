from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from dreamlottracker.services.import_service import ImportService
from dreamlottracker.services.property_service import PropertyService


class ImportPage(QWidget):
    def __init__(self):
        super().__init__()

        self.import_service = ImportService()
        self.property_service = PropertyService()
        self.rows = []

        layout = QVBoxLayout()

        title = QLabel("Import Listings")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")

        subtitle = QLabel("Import properties from CSV or Excel files.")
        subtitle.setStyleSheet("font-size: 14px; color: gray;")

        load_button = QPushButton("Load CSV / Excel File")
        load_button.clicked.connect(self.load_file)

        import_button = QPushButton("Import Listings")
        import_button.clicked.connect(self.import_listings)

        self.status = QLabel("")

        self.preview = QTableWidget(0, 8)
        self.preview.setHorizontalHeaderLabels(
            [
                "Address",
                "City",
                "County",
                "State",
                "Price",
                "Acres",
                "Status",
                "GPS",
            ]
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addWidget(load_button)
        layout.addWidget(import_button)
        layout.addWidget(self.status)
        layout.addWidget(self.preview)

        self.setLayout(layout)

    def load_file(self):
        path_text, _ = QFileDialog.getOpenFileName(
            self,
            "Load Listing File",
            "",
            "Listing Files (*.csv *.xlsx *.xls)",
        )

        if not path_text:
            return

        try:
            self.rows = self.import_service.load_file(Path(path_text))
            self.populate_preview()
            self.status.setText(f"Loaded {len(self.rows)} rows from {Path(path_text).name}")
        except Exception as error:
            QMessageBox.critical(
                self,
                "Import Error",
                str(error),
            )

    def populate_preview(self):
        self.preview.setRowCount(len(self.rows))

        for row_index, row in enumerate(self.rows):
            gps = ""

            if row.get("latitude") and row.get("longitude"):
                gps = f"{row.get('latitude')}, {row.get('longitude')}"

            values = [
                row.get("address", ""),
                row.get("city", ""),
                row.get("county", ""),
                row.get("state", ""),
                row.get("price", ""),
                row.get("acres", ""),
                row.get("status", ""),
                gps,
            ]

            for column, value in enumerate(values):
                self.preview.setItem(row_index, column, QTableWidgetItem(str(value)))

        self.preview.resizeColumnsToContents()

    def import_listings(self):
        if not self.rows:
            QMessageBox.information(
                self,
                "No Data",
                "Please load a CSV or Excel file first.",
            )
            return

        result = self.import_service.import_rows(self.rows)
        self.property_service.recalculate_scores()

        QMessageBox.information(
            self,
            "Import Complete",
            (
                f"Total rows: {result['total']}\\n"
                f"Imported: {result['imported']}\\n"
                f"Skipped: {result['skipped']}"
            ),
        )

        self.status.setText(
            f"Imported {result['imported']} listings. Skipped {result['skipped']}."
        )
