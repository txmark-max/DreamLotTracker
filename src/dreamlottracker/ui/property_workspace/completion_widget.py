from PySide6.QtWidgets import QLabel, QListWidget, QProgressBar, QVBoxLayout, QWidget

from dreamlottracker.services.analysis_service import AnalysisService


class CompletionWidget(QWidget):
    def __init__(self, property_id: int):
        super().__init__()

        self.property_id = property_id
        self.analysis_service = AnalysisService()

        layout = QVBoxLayout()

        title = QLabel("Research Completion")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        analysis = self.analysis_service.analyze_property(property_id)
        missing = analysis.missing_data

        completion = self._completion_percent(missing)
        confidence = self._confidence_percent(completion, missing)

        self.completion_label = QLabel(f"Complete: {completion}%    Confidence: {confidence}%")
        self.completion_label.setStyleSheet("font-size: 13px;")

        self.progress = QProgressBar()
        self.progress.setValue(completion)

        self.missing_list = QListWidget()
        self.missing_list.setMaximumHeight(150)

        if missing:
            for item in missing:
                self.missing_list.addItem(f"☐ {item}")
        else:
            self.missing_list.addItem("✓ No major missing data identified")

        layout.addWidget(title)
        layout.addWidget(self.completion_label)
        layout.addWidget(self.progress)
        layout.addWidget(QLabel("Missing / Next Data Needed"))
        layout.addWidget(self.missing_list)

        self.setLayout(layout)

    def _completion_percent(self, missing: list[str]) -> int:
        expected_items = 16
        missing_count = min(len(missing), expected_items)
        complete = int(((expected_items - missing_count) / expected_items) * 100)
        return max(0, min(100, complete))

    def _confidence_percent(self, completion: int, missing: list[str]) -> int:
        high_impact = {
            "GPS coordinates",
            "Flood zone",
            "Wetlands status",
            "Utility details",
            "Restrictions/HOA details",
            "Financial estimates",
        }

        penalty = sum(5 for item in missing if item in high_impact)
        return max(0, min(100, completion - penalty))
