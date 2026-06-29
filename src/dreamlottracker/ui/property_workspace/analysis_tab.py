from PySide6.QtWidgets import QLabel, QListWidget, QVBoxLayout, QWidget

from dreamlottracker.services.analysis_service import AnalysisService


class AnalysisTab(QWidget):
    def __init__(self, property_id: int):
        super().__init__()

        self.analysis_service = AnalysisService()
        self.property_id = property_id

        layout = QVBoxLayout()
        analysis = self.analysis_service.analyze_property(property_id)

        headline = QLabel(
            f"Recommendation: {analysis.recommendation}    "
            f"Suggested Offer: ${analysis.suggested_offer:,.0f}    "
            f"Max Offer: ${analysis.maximum_offer:,.0f}    "
            f"Negotiation: {analysis.negotiation_strength}"
        )
        headline.setStyleSheet("font-size: 16px; font-weight: bold;")

        summary = QLabel(analysis.summary)
        summary.setWordWrap(True)
        summary.setStyleSheet("font-size: 14px;")

        layout.addWidget(headline)
        layout.addWidget(summary)
        layout.addSpacing(10)
        layout.addWidget(self._list_section("Strengths", analysis.strengths))
        layout.addWidget(self._list_section("Concerns", analysis.concerns))
        layout.addWidget(self._list_section("Missing Data", analysis.missing_data))
        layout.addWidget(self._list_section("Due Diligence", analysis.due_diligence))
        layout.addStretch()

        self.setLayout(layout)

    def _list_section(self, title: str, items: list[str]) -> QListWidget:
        box = QListWidget()
        box.addItem(f"--- {title} ---")
        for item in items:
            box.addItem(f"• {item}")
        return box
