from PySide6.QtWidgets import QLabel, QListWidget, QProgressBar, QVBoxLayout, QWidget

from dreamlottracker.services.analysis_service import AnalysisService


class CompletionWidget(QWidget):
    def __init__(self, property_id):
        super().__init__()

        analysis = AnalysisService().analyze_property(property_id)
        missing = analysis.missing_data
        completion = self._completion_percent(missing)
        confidence = self._confidence_percent(completion, missing)

        layout = QVBoxLayout()

        title = QLabel("Research Completion")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        label = QLabel(f"Complete: {completion}%    Confidence: {confidence}%")
        progress = QProgressBar()
        progress.setValue(completion)

        missing_list = QListWidget()
        missing_list.setMaximumHeight(150)

        if missing:
            for item in missing:
                missing_list.addItem(f"☐ {item}")
        else:
            missing_list.addItem("✓ No major missing data identified")

        layout.addWidget(title)
        layout.addWidget(label)
        layout.addWidget(progress)
        layout.addWidget(QLabel("Missing / Next Data Needed"))
        layout.addWidget(missing_list)
        self.setLayout(layout)

    def _completion_percent(self, missing):
        expected_items = 16
        return max(0, min(100, int(((expected_items - min(len(missing), expected_items)) / expected_items) * 100)))

    def _confidence_percent(self, completion, missing):
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
