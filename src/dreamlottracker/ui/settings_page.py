from PySide6.QtWidgets import (
    QDoubleSpinBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from dreamlottracker.services.settings_service import SettingsService


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.service = SettingsService()

        outer_layout = QVBoxLayout()

        title = QLabel("Settings")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")

        subtitle = QLabel("Search criteria, Dream Engine weights, and drive-time automation")
        subtitle.setStyleSheet("font-size: 14px; color: gray;")

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content = QWidget()
        layout = QVBoxLayout()

        criteria_title = QLabel("Search Criteria")
        criteria_title.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.max_price = self._money()
        self.target_price_per_acre = self._money()
        self.min_acres = self._double()
        self.max_acres = self._double()
        self.ideal_acres = self._double()
        self.max_distance = self._integer(" miles")
        self.target_drive_minutes = self._integer(" minutes")
        self.max_hoa = self._money()
        self.minimum_dream_score = self._integer()
        self.preferred_cities = QLineEdit()

        criteria_form = QFormLayout()
        criteria_form.addRow("Maximum Lot Price", self.max_price)
        criteria_form.addRow("Target Price Per Acre", self.target_price_per_acre)
        criteria_form.addRow("Minimum Acres", self.min_acres)
        criteria_form.addRow("Maximum Acres", self.max_acres)
        criteria_form.addRow("Ideal Acres", self.ideal_acres)
        criteria_form.addRow("Maximum Distance", self.max_distance)
        criteria_form.addRow("Target Drive Time to Gulf Shores", self.target_drive_minutes)
        criteria_form.addRow("Maximum HOA", self.max_hoa)
        criteria_form.addRow("Minimum Dream Score", self.minimum_dream_score)
        criteria_form.addRow("Preferred Cities", self.preferred_cities)

        scoring_title = QLabel("Dream Engine Weights")
        scoring_title.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.weight_price = self._integer()
        self.weight_location = self._integer()
        self.weight_utilities = self._integer()
        self.weight_flood = self._integer()
        self.weight_restrictions = self._integer()
        self.weight_buildability = self._integer()

        scoring_form = QFormLayout()
        scoring_form.addRow("Price / Value Weight", self.weight_price)
        scoring_form.addRow("Location / Drive Time Weight", self.weight_location)
        scoring_form.addRow("Utilities Weight", self.weight_utilities)
        scoring_form.addRow("Flood / Wetlands Weight", self.weight_flood)
        scoring_form.addRow("Restrictions Weight", self.weight_restrictions)
        scoring_form.addRow("Buildability Weight", self.weight_buildability)

        drive_title = QLabel("Drive Time Automation")
        drive_title.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.ors_api_key = QLineEdit()
        self.ors_api_key.setEchoMode(QLineEdit.Password)

        self.destination_gulf_shores_lat = self._coordinate()
        self.destination_gulf_shores_lon = self._coordinate()
        self.destination_foley_lat = self._coordinate()
        self.destination_foley_lon = self._coordinate()
        self.destination_fairhope_lat = self._coordinate()
        self.destination_fairhope_lon = self._coordinate()
        self.destination_pensacola_lat = self._coordinate()
        self.destination_pensacola_lon = self._coordinate()

        drive_note = QLabel(
            "OpenRouteService is used for drive-time calculations. Destination coordinates are editable "
            "so you can target specific places like the beach, courthouse, airport, or downtown."
        )
        drive_note.setWordWrap(True)
        drive_note.setStyleSheet("color: gray; font-style: italic;")

        drive_form = QFormLayout()
        drive_form.addRow("OpenRouteService API Key", self.ors_api_key)
        drive_form.addRow("Gulf Shores Latitude", self.destination_gulf_shores_lat)
        drive_form.addRow("Gulf Shores Longitude", self.destination_gulf_shores_lon)
        drive_form.addRow("Foley Latitude", self.destination_foley_lat)
        drive_form.addRow("Foley Longitude", self.destination_foley_lon)
        drive_form.addRow("Fairhope Latitude", self.destination_fairhope_lat)
        drive_form.addRow("Fairhope Longitude", self.destination_fairhope_lon)
        drive_form.addRow("Pensacola Latitude", self.destination_pensacola_lat)
        drive_form.addRow("Pensacola Longitude", self.destination_pensacola_lon)

        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save)

        self.status = QLabel("")
        self.status.setStyleSheet("color: green;")

        layout.addWidget(criteria_title)
        layout.addLayout(criteria_form)
        layout.addSpacing(18)
        layout.addWidget(scoring_title)
        layout.addLayout(scoring_form)
        layout.addSpacing(18)
        layout.addWidget(drive_title)
        layout.addWidget(drive_note)
        layout.addLayout(drive_form)
        layout.addSpacing(18)
        layout.addWidget(save_button)
        layout.addWidget(self.status)
        layout.addStretch()

        content.setLayout(layout)
        scroll.setWidget(content)

        outer_layout.addWidget(title)
        outer_layout.addWidget(subtitle)
        outer_layout.addSpacing(10)
        outer_layout.addWidget(scroll)

        self.setLayout(outer_layout)
        self.load()

    def load(self):
        settings = self.service.get_settings()

        self.max_price.setValue(float(settings.get("max_price", "125000")))
        self.target_price_per_acre.setValue(float(settings.get("target_price_per_acre", "90000")))
        self.min_acres.setValue(float(settings.get("min_acres", "0.5")))
        self.max_acres.setValue(float(settings.get("max_acres", "2.0")))
        self.ideal_acres.setValue(float(settings.get("ideal_acres", "1.25")))
        self.max_distance.setValue(int(float(settings.get("max_distance_miles", "45"))))
        self.target_drive_minutes.setValue(int(float(settings.get("target_drive_minutes_gulf_shores", "45"))))
        self.max_hoa.setValue(float(settings.get("max_hoa", "0")))
        self.minimum_dream_score.setValue(int(float(settings.get("minimum_dream_score", "85"))))
        self.preferred_cities.setText(settings.get("preferred_cities", ""))

        self.weight_price.setValue(int(float(settings.get("weight_price", "28"))))
        self.weight_location.setValue(int(float(settings.get("weight_location", "22"))))
        self.weight_utilities.setValue(int(float(settings.get("weight_utilities", "15"))))
        self.weight_flood.setValue(int(float(settings.get("weight_flood", "12"))))
        self.weight_restrictions.setValue(int(float(settings.get("weight_restrictions", "13"))))
        self.weight_buildability.setValue(int(float(settings.get("weight_buildability", "10"))))

        self.ors_api_key.setText(settings.get("ors_api_key", ""))

        self.destination_gulf_shores_lat.setValue(float(settings.get("destination_gulf_shores_lat", "30.2460")))
        self.destination_gulf_shores_lon.setValue(float(settings.get("destination_gulf_shores_lon", "-87.7008")))
        self.destination_foley_lat.setValue(float(settings.get("destination_foley_lat", "30.4066")))
        self.destination_foley_lon.setValue(float(settings.get("destination_foley_lon", "-87.6836")))
        self.destination_fairhope_lat.setValue(float(settings.get("destination_fairhope_lat", "30.5229")))
        self.destination_fairhope_lon.setValue(float(settings.get("destination_fairhope_lon", "-87.9033")))
        self.destination_pensacola_lat.setValue(float(settings.get("destination_pensacola_lat", "30.4213")))
        self.destination_pensacola_lon.setValue(float(settings.get("destination_pensacola_lon", "-87.2169")))

    def save(self):
        self.service.save_settings(
            {
                "max_price": str(self.max_price.value()),
                "target_price_per_acre": str(self.target_price_per_acre.value()),
                "min_acres": str(self.min_acres.value()),
                "max_acres": str(self.max_acres.value()),
                "ideal_acres": str(self.ideal_acres.value()),
                "max_distance_miles": str(self.max_distance.value()),
                "target_drive_minutes_gulf_shores": str(self.target_drive_minutes.value()),
                "max_hoa": str(self.max_hoa.value()),
                "minimum_dream_score": str(self.minimum_dream_score.value()),
                "preferred_cities": self.preferred_cities.text().strip(),
                "weight_price": str(self.weight_price.value()),
                "weight_location": str(self.weight_location.value()),
                "weight_utilities": str(self.weight_utilities.value()),
                "weight_flood": str(self.weight_flood.value()),
                "weight_restrictions": str(self.weight_restrictions.value()),
                "weight_buildability": str(self.weight_buildability.value()),
                "ors_api_key": self.ors_api_key.text().strip(),
                "destination_gulf_shores_lat": str(self.destination_gulf_shores_lat.value()),
                "destination_gulf_shores_lon": str(self.destination_gulf_shores_lon.value()),
                "destination_foley_lat": str(self.destination_foley_lat.value()),
                "destination_foley_lon": str(self.destination_foley_lon.value()),
                "destination_fairhope_lat": str(self.destination_fairhope_lat.value()),
                "destination_fairhope_lon": str(self.destination_fairhope_lon.value()),
                "destination_pensacola_lat": str(self.destination_pensacola_lat.value()),
                "destination_pensacola_lon": str(self.destination_pensacola_lon.value()),
            }
        )

        self.status.setText("Settings saved.")

    def _money(self):
        widget = QDoubleSpinBox()
        widget.setMaximum(100_000_000)
        widget.setPrefix("$")
        widget.setDecimals(0)
        return widget

    def _double(self):
        widget = QDoubleSpinBox()
        widget.setMaximum(1000)
        widget.setDecimals(2)
        return widget

    def _coordinate(self):
        widget = QDoubleSpinBox()
        widget.setRange(-180, 180)
        widget.setDecimals(6)
        return widget

    def _integer(self, suffix: str = ""):
        widget = QSpinBox()
        widget.setMaximum(10000)
        if suffix:
            widget.setSuffix(suffix)
        return widget
