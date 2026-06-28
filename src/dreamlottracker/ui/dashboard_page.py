from PySide6.QtWidgets import (
    QLabel,
    QGridLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from dreamlottracker.services.property_service import PropertyService


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()

        self.service = PropertyService()

        layout = QVBoxLayout()

        title = QLabel("Dashboard")
        title.setStyleSheet(
            "font-size: 28px; font-weight: bold;"
        )

        subtitle = QLabel("Live database overview")
        subtitle.setStyleSheet(
            "font-size: 14px; color: gray;"
        )

        stats = QGridLayout()

        self.total_card = self.create_card("Properties")
        self.active_card = self.create_card("Active")
        self.dream_card = self.create_card("Dream Lots")
        self.average_card = self.create_card("Average Score")

        stats.addWidget(self.total_card, 0, 0)
        stats.addWidget(self.active_card, 0, 1)
        stats.addWidget(self.dream_card, 0, 2)
        stats.addWidget(self.average_card, 0, 3)

        refresh = QPushButton("Refresh")
        refresh.clicked.connect(self.refresh)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addLayout(stats)
        layout.addWidget(refresh)
        layout.addStretch()

        self.setLayout(layout)

        self.refresh()

    def create_card(self, label):
        card = QLabel(f"0\n{label}")
        card.setMinimumWidth(150)
        card.setStyleSheet("""
            QLabel {
                border: 1px solid #C0C0C0;
                border-radius: 8px;
                padding: 20px;
                font-size: 18px;
            }
        """)
        return card

    def refresh(self):
        stats = self.service.get_dashboard_stats()

        self.total_card.setText(
            f"{stats['total']}\nProperties"
        )

        self.active_card.setText(
            f"{stats['active']}\nActive"
        )

        self.dream_card.setText(
            f"{stats['dream_lots']}\nDream Lots"
        )

        self.average_card.setText(
            f"{stats['average_score']:.1f}\nAverage Score"
        )
