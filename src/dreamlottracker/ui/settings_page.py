from PySide6.QtWidgets import (
    QDoubleSpinBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from dreamlottracker.services.settings_service import SettingsService


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.service = SettingsService()

        layout = QVBoxLayout()

        title = QLabel("Settings")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")

        subtitle = QLabel("Search criteria and scoring preferences")
        subtitle.setStyleSheet("font-size: 14px; color: gray;")

        self.max_price = QDoubleSpinBox()
        self.max_price.setMaximum(10_000_000)
        self.max_price.setPrefix("$")
        self.max_price.setDecimals(0)

        self.min_acres = QDoubleSpinBox()
        self.min_acres.setMaximum(1000)
        self.min_acres.setDecimals(2)

        self.max_acres = QDoubleSpinBox()
        self.max_acres.setMaximum(1000)
        self.max_acres.setDecimals(2)

        self.max_distance = QSpinBox()
        self.max_distance.setMaximum(1000)
        self.max_distance.setSuffix(" miles")

        self.max_hoa = QDoubleSpinBox()
        self.max_hoa.setMaximum(100_000)
        self.max_hoa.setPrefix("$")
        self.max_hoa.setDecimals(0)

        self.minimum_dream_score = QSpinBox()
        self.minimum_dream_score.setMaximum(100)

        self.preferred_cities = QLineEdit()

        form = QFormLayout()
        form.addRow("Maximum Lot Price", self.max_price)
        form.addRow("Minimum Acres", self.min_acres)
        form.addRow("Maximum Acres", self.max_acres)
        form.addRow("Maximum Distance", self.max_distance)
        form.addRow("Maximum HOA", self.max_hoa)
        form.addRow("Minimum Dream Score", self.minimum_dream_score)
        form.addRow("Preferred Cities", self.preferred_cities)

        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save)

        self.status = QLabel("")
        self.status.setStyleSheet("color: green;")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addLayout(form)
        layout.addWidget(save_button)
        layout.addWidget(self.status)
        layout.addStretch()

        self.setLayout(layout)

        self.load()

    def load(self):
        settings = self.service.get_settings()

        self.max_price.setValue(float(settings.get("max_price", "125000")))
        self.min_acres.setValue(float(settings.get("min_acres", "0.5")))
        self.max_acres.setValue(float(settings.get("max_acres", "2.0")))
        self.max_distance.setValue(int(float(settings.get("max_distance_miles", "45"))))
        self.max_hoa.setValue(float(settings.get("max_hoa", "0")))
        self.minimum_dream_score.setValue(
            int(float(settings.get("minimum_dream_score", "85")))
        )
        self.preferred_cities.setText(settings.get("preferred_cities", ""))

    def save(self):
        self.service.save_settings(
            {
                "max_price": str(self.max_price.value()),
                "min_acres": str(self.min_acres.value()),
                "max_acres": str(self.max_acres.value()),
                "max_distance_miles": str(self.max_distance.value()),
                "max_hoa": str(self.max_hoa.value()),
                "minimum_dream_score": str(self.minimum_dream_score.value()),
                "preferred_cities": self.preferred_cities.text().strip(),
            }
        )

        self.status.setText("Settings saved.")
