from PySide6.QtWidgets import QLabel, QListWidget, QVBoxLayout, QWidget

from dreamlottracker.services.analysis_service import AnalysisService


class AnalysisTab(QWidget):
    def __init__(self, property_id):
        super().__init__()

        analysis = AnalysisService().analyze_property(property_id)

        layout = QVBoxLayout()

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
        layout.addWidget(self._section("Strengths", analysis.strengths))
        layout.addWidget(self._section("Concerns", analysis.concerns))
        layout.addWidget(self._section("Missing Data", analysis.missing_data))
        layout.addWidget(self._section("Due Diligence", analysis.due_diligence))
        self.setLayout(layout)

    def _section(self, title, items):
        widget = QListWidget()
        widget.addItem(f"--- {title} ---")
        for item in items:
            widget.addItem(f"• {item}")
        return widget
