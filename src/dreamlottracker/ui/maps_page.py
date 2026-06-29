from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from dreamlottracker.services.map_export_service import MapExportService


class MapsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.export_service = MapExportService()

        layout = QVBoxLayout()

        title = QLabel("Maps")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")

        subtitle = QLabel("Export properties with GPS coordinates to Google Earth KML.")
        subtitle.setStyleSheet("font-size: 14px; color: gray;")

        export_button = QPushButton("Export Google Earth KML")
        export_button.clicked.connect(self.export_kml)

        note = QLabel(
            "Only properties with latitude and longitude saved in the Property Workspace will appear in the KML."
        )
        note.setWordWrap(True)

        self.status = QLabel("")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addWidget(export_button)
        layout.addWidget(note)
        layout.addWidget(self.status)
        layout.addStretch()

        self.setLayout(layout)

    def export_kml(self):
        path_text, _ = QFileDialog.getSaveFileName(
            self,
            "Export KML",
            "DreamLotTracker_Properties.kml",
            "KML Files (*.kml)",
        )

        if not path_text:
            return

        path = Path(path_text)

        if path.suffix.lower() != ".kml":
            path = path.with_suffix(".kml")

        exported = self.export_service.export_kml(path)
        self.status.setText(f"Exported to {exported}")

        QMessageBox.information(
            self,
            "KML Export Complete",
            f"KML exported to:\n{exported}",
        )
