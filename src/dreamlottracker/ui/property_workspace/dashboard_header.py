from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QVBoxLayout, QWidget

from dreamlottracker.services.analysis_service import AnalysisService


class DashboardHeader(QWidget):
    def __init__(self, property_):
        super().__init__()

        self.property_ = property_
        self.analysis_service = AnalysisService()

        layout = QVBoxLayout()

        title = QLabel(self._title_text())
        title.setStyleSheet("font-size: 26px; font-weight: bold;")

        subtitle = QLabel(self._subtitle_text())
        subtitle.setStyleSheet("font-size: 14px; color: gray;")

        score = self._score_text()
        score.setStyleSheet("font-size: 18px; font-weight: bold;")

        cards = QGridLayout()
        card_values = self._card_values()

        for index, (label, value) in enumerate(card_values):
            cards.addWidget(self._card(label, value), index // 3, index % 3)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(score)
        layout.addSpacing(8)
        layout.addLayout(cards)

        self.setLayout(layout)

    def _title_text(self) -> str:
        return self.property_.address or "Property"

    def _subtitle_text(self) -> str:
        city = self.property_.city or ""
        state = self.property_.state or ""
        acres = float(self.property_.acres or 0)
        return f"{city}, {state}  •  {acres:.2f} acres"

    def _score_text(self) -> QLabel:
        scores = self.property_.scores
        dream_score = scores.dream_score if scores and scores.dream_score is not None else 0
        recommendation = scores.recommendation if scores and scores.recommendation else "Not Scored"

        stars = self._stars(dream_score)
        return QLabel(f"{stars}  {recommendation}  •  Dream Score: {dream_score:.1f}")

    def _stars(self, score: float) -> str:
        if score >= 95:
            return "★★★★★"
        if score >= 90:
            return "★★★★☆"
        if score >= 82:
            return "★★★☆☆"
        return "★★☆☆☆"

    def _card_values(self):
        listing = self.property_.listings[0] if self.property_.listings else None
        scores = self.property_.scores
        location = self.property_.location_metrics
        utilities = self.property_.utilities
        restrictions = self.property_.restrictions

        price = listing.asking_price if listing else 0
        acres = self.property_.acres or 0
        price_per_acre = price / acres if acres else 0

        minutes = location.minutes_to_gulf_shores if location and location.minutes_to_gulf_shores else None
        drive = f"{minutes} min" if minutes else "Unknown"

        flood = location.flood_zone if location and location.flood_zone else "Unknown"

        if restrictions and restrictions.hoa:
            hoa = restrictions.hoa
        else:
            hoa = "Unknown"

        utility_bits = []
        if utilities:
            if utilities.electric in ("At Road", "Available"):
                utility_bits.append("Electric")
            if utilities.county_water == "Available":
                utility_bits.append("Water")
            if utilities.fiber == "Available":
                utility_bits.append("Fiber")
        utilities_text = ", ".join(utility_bits) if utility_bits else "Unknown"

        score = scores.dream_score if scores and scores.dream_score is not None else 0

        return [
            ("Price", f"${price:,.0f}"),
            ("Price / Acre", f"${price_per_acre:,.0f}"),
            ("Drive to Gulf Shores", drive),
            ("Flood Zone", flood),
            ("HOA", hoa),
            ("Utilities", utilities_text),
            ("Dream Score", f"{score:.1f}"),
            ("Acres", f"{acres:.2f}"),
            ("City", self.property_.city or ""),
        ]

    def _card(self, label: str, value: str) -> QFrame:
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet("""
            QFrame {
                border: 1px solid #C8C8C8;
                border-radius: 8px;
                padding: 10px;
            }
        """)

        layout = QVBoxLayout()
        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        label_label = QLabel(label)
        label_label.setStyleSheet("font-size: 12px; color: gray;")

        layout.addWidget(value_label)
        layout.addWidget(label_label)
        frame.setLayout(layout)

        return frame
