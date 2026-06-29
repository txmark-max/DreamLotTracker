from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QVBoxLayout, QWidget


class DashboardHeader(QWidget):
    def __init__(self, property_):
        super().__init__()
        self.property_ = property_

        layout = QVBoxLayout()

        title = QLabel(property_.address or "Property")
        title.setStyleSheet("font-size: 26px; font-weight: bold;")

        subtitle = QLabel(f"{property_.city or ''}, {property_.state or ''} • {float(property_.acres or 0):.2f} acres")
        subtitle.setStyleSheet("font-size: 14px; color: gray;")

        scores = property_.scores
        score = scores.dream_score if scores and scores.dream_score is not None else 0
        recommendation = scores.recommendation if scores and scores.recommendation else "Not Scored"

        score_label = QLabel(f"{self._stars(score)}  {recommendation}  •  Dream Score: {score:.1f}")
        score_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        cards = QGridLayout()
        for index, (label, value) in enumerate(self._card_values()):
            cards.addWidget(self._card(label, value), index // 3, index % 3)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(score_label)
        layout.addLayout(cards)
        self.setLayout(layout)

    def _stars(self, score):
        if score >= 95:
            return "★★★★★"
        if score >= 90:
            return "★★★★☆"
        if score >= 82:
            return "★★★☆☆"
        return "★★☆☆☆"

    def _card_values(self):
        prop = self.property_
        listing = prop.listings[0] if prop.listings else None
        location = prop.location_metrics
        utilities = prop.utilities
        restrictions = prop.restrictions
        scores = prop.scores

        price = listing.asking_price if listing else 0
        acres = prop.acres or 0
        price_per_acre = price / acres if acres else 0
        minutes = location.minutes_to_gulf_shores if location and location.minutes_to_gulf_shores else None
        drive = f"{minutes} min" if minutes else "Unknown"
        flood = location.flood_zone if location and location.flood_zone else "Unknown"
        hoa = restrictions.hoa if restrictions and restrictions.hoa else "Unknown"

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
            ("City", prop.city or ""),
        ]

    def _card(self, label, value):
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet("QFrame { border: 1px solid #C8C8C8; border-radius: 8px; padding: 10px; }")

        layout = QVBoxLayout()
        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        label_label = QLabel(label)
        label_label.setStyleSheet("font-size: 12px; color: gray;")

        layout.addWidget(value_label)
        layout.addWidget(label_label)
        frame.setLayout(layout)
        return frame
