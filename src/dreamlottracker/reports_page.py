from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from dreamlottracker.services.export_service import ExportService
from dreamlottracker.services.pdf_report_service import PDFReportService
from dreamlottracker.services.property_service import PropertyService


class ReportsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.export_service = ExportService()
        self.pdf_service = PDFReportService()
        self.property_service = PropertyService()
        self.properties = []

        layout = QVBoxLayout()

        title = QLabel("Reports")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")

        subtitle = QLabel("Export property data and printable property reports")
        subtitle.setStyleSheet("font-size: 14px; color: gray;")

        export_button = QPushButton("Export Properties to Excel")
        export_button.clicked.connect(self.export_properties)

        self.property_list = QListWidget()

        refresh_button = QPushButton("Refresh Property List")
        refresh_button.clicked.connect(self.load_properties)

        pdf_button = QPushButton("Export Selected Property PDF")
        pdf_button.clicked.connect(self.export_selected_pdf)

        self.status = QLabel("")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addWidget(export_button)
        layout.addSpacing(20)
        layout.addWidget(QLabel("Property Reports"))
        layout.addWidget(self.property_list)
        layout.addWidget(refresh_button)
        layout.addWidget(pdf_button)
        layout.addWidget(self.status)
        layout.addStretch()

        self.setLayout(layout)

        self.load_properties()

    def load_properties(self):
        self.property_list.clear()
        self.properties = self.property_service.get_all_properties()

        for property_ in self.properties:
            listing = property_.listings[0] if property_.listings else None
            price = listing.asking_price if listing else 0
            item = QListWidgetItem(
                f"{property_.address} — {property_.city} — ${price:,.0f}"
            )
            item.setData(1000, property_.id)
            self.property_list.addItem(item)

    def export_properties(self):
        path_text, _ = QFileDialog.getSaveFileName(
            self,
            "Export Properties",
            "DreamLotTracker_Properties.xlsx",
            "Excel Files (*.xlsx)",
        )

        if not path_text:
            return

        path = Path(path_text)

        if path.suffix.lower() != ".xlsx":
            path = path.with_suffix(".xlsx")

        exported = self.export_service.export_properties_to_excel(path)

        self.status.setText(f"Exported to {exported}")

        QMessageBox.information(
            self,
            "Export Complete",
            f"Properties exported to:\n{exported}",
        )

    def export_selected_pdf(self):
        selected = self.property_list.selectedItems()

        if not selected:
            QMessageBox.information(
                self,
                "No Selection",
                "Please select a property to export.",
            )
            return

        property_id = selected[0].data(1000)

        property_ = next(
            (item for item in self.properties if item.id == property_id),
            None,
        )

        default_name = "PropertyReport.pdf"

        if property_:
            safe_address = property_.address.replace("/", "-").replace(" ", "_")
            default_name = f"{safe_address}_Report.pdf"

        path_text, _ = QFileDialog.getSaveFileName(
            self,
            "Export Property Report",
            default_name,
            "PDF Files (*.pdf)",
        )

        if not path_text:
            return

        path = Path(path_text)

        if path.suffix.lower() != ".pdf":
            path = path.with_suffix(".pdf")

        exported = self.pdf_service.export_property_report(property_id, path)

        self.status.setText(f"Exported PDF to {exported}")

        QMessageBox.information(
            self,
            "PDF Export Complete",
            f"Property report exported to:\n{exported}",
        )
