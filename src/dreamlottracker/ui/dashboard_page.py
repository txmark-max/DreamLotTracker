from PySide6.QtWidgets import QLabel, QGridLayout, QVBoxLayout, QWidget


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("Dashboard")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")

        subtitle = QLabel("Dream Lot Tracker v6.1 Alpha")
        subtitle.setStyleSheet("font-size: 14px; color: gray;")

        stats = QGridLayout()
        stats.addWidget(self._stat_card("Properties", "0"), 0, 0)
        stats.addWidget(self._stat_card("Average Score", "—"), 0, 1)
        stats.addWidget(self._stat_card("Dream Lots", "0"), 0, 2)
        stats.addWidget(self._stat_card("Price Drops", "0"), 0, 3)

        empty = QLabel("No properties loaded yet.")
        empty.setStyleSheet("font-size: 16px; margin-top: 30px;")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addLayout(stats)
        layout.addWidget(empty)
        layout.addStretch()

        self.setLayout(layout)

    def _stat_card(self, label: str, value: str) -> QWidget:
        card = QWidget()
        card.setStyleSheet("""
            QWidget {
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 12px;
            }
        """)

        layout = QVBoxLayout()

        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 26px; font-weight: bold;")

        text_label = QLabel(label)
        text_label.setStyleSheet("font-size: 13px; color: gray;")

        layout.addWidget(value_label)
        layout.addWidget(text_label)

        card.setLayout(layout)
        return card
