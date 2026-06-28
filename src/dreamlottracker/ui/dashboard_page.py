from PySide6.QtWidgets import QLabel, QGridLayout, QPushButton, QVBoxLayout, QWidget

from dreamlottracker.repositories.property_repository import PropertyRepository


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()

        self.repository = PropertyRepository()

        layout = QVBoxLayout()

        title = QLabel("Dashboard")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")

        subtitle = QLabel("Live database overview")
        subtitle.setStyleSheet("font-size: 14px; color: gray;")

        self.stats = QGridLayout()

        self.total_card = self._stat_card("Properties", "0")
        self.active_card = self._stat_card("Active", "0")
        self.dream_card = self._stat_card("Dream Lots", "0")
        self.avg_card = self._stat_card("Average Score", "—")

        self.stats.addWidget(self.total_card, 0, 0)
        self.stats.addWidget(self.active_card, 0, 1)
        self.stats.addWidget(self.dream_card, 0, 2)
        self.stats.addWidget(self.avg_card, 0, 3)

        refresh = QPushButton("Refresh Dashboard")
        refresh.clicked.connect(self.refresh)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addLayout(self.stats)
        layout.addSpacing(20)
        layout.addWidget(refresh)
        layout.addStretch()

        self.setLayout(layout)

        self.refresh()

    def _stat_card(self, label: str, value: str) -> QLabel:
        card = QLabel(f"{value}\n{label}")
        card.setStyleSheet("""
            QLabel {
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 18px;
                font-size: 18px;
                min-width: 140px;
            }
        """)
        return card

    def refresh(self):
        total = self.repository.count()
        active = self.repository.active_count()
        dream_lots = self.repository.dream_lot_count()
        avg_score = self.repository.average_score()

        self.total_card.setText(f"{total}\nProperties")
        self.active_card.setText(f"{active}\nActive")
        self.dream_card.setText(f"{dream_lots}\nDream Lots")
        self.avg_card.setText(f"{avg_score:.1f}\nAverage Score")
