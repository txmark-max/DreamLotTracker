from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from dreamlottracker.services.export_service import ExportService


class ReportsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.export_service = ExportService()

        layout = QVBoxLayout()

        title = QLabel("Reports")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")

        subtitle = QLabel("Export property data for review and sharing")
        subtitle.setStyleSheet("font-size: 14px; color: gray;")

        export_button = QPushButton("Export Properties to Excel")
        export_button.clicked.connect(self.export_properties)

        self.status = QLabel("")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addWidget(export_button)
        layout.addWidget(self.status)
        layout.addStretch()

        self.setLayout(layout)

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
