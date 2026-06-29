from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from dreamlottracker.services.drive_time_service import DriveTimeService
from dreamlottracker.services.gis_fema_service import GISFEMAService
from dreamlottracker.ui.property_workspace.form_helpers import check, combo, spin


class LocationTab(QWidget):
    def __init__(self, property_):
        super().__init__()

        self.property_ = property_
        self.drive_time_service = DriveTimeService()
        self.gis_fema_service = GISFEMAService()

        loc = property_.location_metrics

        layout = QVBoxLayout()
        form = QFormLayout()

        self.minutes_to_gulf_shores = spin(
            loc.minutes_to_gulf_shores
            if loc and loc.minutes_to_gulf_shores
            else 0
        )
        self.minutes_to_foley = spin(
            loc.minutes_to_foley if loc and loc.minutes_to_foley else 0
        )
        self.minutes_to_fairhope = spin(
            loc.minutes_to_fairhope if loc and loc.minutes_to_fairhope else 0
        )
        self.minutes_to_pensacola = spin(
            loc.minutes_to_pensacola if loc and loc.minutes_to_pensacola else 0
        )
        self.flood_zone = combo(
            ["Unknown", "X", "AE", "VE"],
            loc.flood_zone if loc and loc.flood_zone else "Unknown",
        )
        self.wetlands = combo(
            ["Unknown", "None", "Possible", "Confirmed"],
            loc.wetlands if loc and loc.wetlands else "Unknown",
        )
        self.road_type = combo(
            ["Unknown", "County", "Private", "State"],
            loc.road_type if loc and loc.road_type else "Unknown",
        )
        self.paved_road = check(loc.paved_road if loc else None)

        calculate_button = QPushButton("Calculate Drive Times")
        calculate_button.clicked.connect(self.calculate_drive_times)

        form.addRow("Minutes to Gulf Shores", self.minutes_to_gulf_shores)
        form.addRow("Minutes to Foley", self.minutes_to_foley)
        form.addRow("Minutes to Fairhope", self.minutes_to_fairhope)
        form.addRow("Minutes to Pensacola", self.minutes_to_pensacola)
        form.addRow("", calculate_button)
        form.addRow("Flood Zone", self.flood_zone)
        form.addRow("Wetlands", self.wetlands)
        form.addRow("Road Type", self.road_type)
        form.addRow("Paved Road", self.paved_road)

        note = QLabel(
            "Drive time is used for scoring. Flood zone and wetlands should be "
            "verified using FEMA, county GIS, surveys, or professional due diligence."
        )
        note.setWordWrap(True)
        note.setMinimumHeight(70)
        note.setStyleSheet("color: gray; font-style: italic;")
        form.addRow("", note)

        gis_title = QLabel("GIS / FEMA Verification Tools")
        gis_title.setStyleSheet("font-size: 16px; font-weight: bold;")

        search_text = self.gis_fema_service.fema_search_text(self.property_)
        search_label = QLabel(
            f"FEMA search text copied when opening MSC: {search_text or 'No address/GPS available'}"
        )
        search_label.setWordWrap(True)
        search_label.setStyleSheet("color: gray;")

        button_row_1 = QHBoxLayout()
        fema_msc_button = QPushButton("Open FEMA MSC")
        fema_msc_button.clicked.connect(self.open_fema_msc)

        fema_nfhl_button = QPushButton("Open FEMA NFHL Viewer")
        fema_nfhl_button.clicked.connect(self.open_fema_nfhl)

        button_row_1.addWidget(fema_msc_button)
        button_row_1.addWidget(fema_nfhl_button)

        button_row_2 = QHBoxLayout()
        baldwin_gis_button = QPushButton("Open Baldwin Parcel Viewer")
        baldwin_gis_button.clicked.connect(self.open_baldwin_parcel_viewer)

        baldwin_property_button = QPushButton("Open Baldwin Property Search")
        baldwin_property_button.clicked.connect(self.open_baldwin_property_search)

        button_row_2.addWidget(baldwin_gis_button)
        button_row_2.addWidget(baldwin_property_button)

        help_text = QLabel(
            "Tip: FEMA MSC can be searched by address or by coordinates. "
            "When opening FEMA MSC, the app copies the best available search text "
            "to your clipboard so you can paste it into FEMA's search box."
        )
        help_text.setWordWrap(True)
        help_text.setStyleSheet("color: gray; font-style: italic;")

        layout.addLayout(form)
        layout.addSpacing(14)
        layout.addWidget(gis_title)
        layout.addWidget(search_label)
        layout.addLayout(button_row_1)
        layout.addLayout(button_row_2)
        layout.addWidget(help_text)
        layout.addStretch()

        self.setLayout(layout)

    def calculate_drive_times(self):
        try:
            result = self.drive_time_service.calculate_drive_times(
                latitude=self.property_.latitude,
                longitude=self.property_.longitude,
            )
        except Exception as error:
            QMessageBox.critical(self, "Drive Time Error", str(error))
            return

        self.minutes_to_gulf_shores.setValue(result.get("gulf_shores", 0))
        self.minutes_to_foley.setValue(result.get("foley", 0))
        self.minutes_to_fairhope.setValue(result.get("fairhope", 0))
        self.minutes_to_pensacola.setValue(result.get("pensacola", 0))

        QMessageBox.information(
            self,
            "Drive Times Calculated",
            "Drive times were calculated. Click Save to store them with this property.",
        )

    def open_fema_msc(self):
        self.gis_fema_service.open_fema_map_service_center(self.property_)
        QMessageBox.information(
            self,
            "FEMA MSC Opened",
            "FEMA Map Service Center opened. The best available search text was copied to your clipboard.",
        )

    def open_fema_nfhl(self):
        self.gis_fema_service.open_fema_nfhl_viewer(self.property_)

    def open_baldwin_parcel_viewer(self):
        self.gis_fema_service.open_baldwin_parcel_viewer(self.property_)

    def open_baldwin_property_search(self):
        self.gis_fema_service.open_baldwin_property_search(self.property_)

    def values(self):
        return {
            "miles_to_gulf_shores": 0,
            "minutes_to_gulf_shores": int(self.minutes_to_gulf_shores.value()),
            "minutes_to_foley": int(self.minutes_to_foley.value()),
            "minutes_to_fairhope": int(self.minutes_to_fairhope.value()),
            "minutes_to_pensacola": int(self.minutes_to_pensacola.value()),
            "flood_zone": self.flood_zone.currentText(),
            "wetlands": self.wetlands.currentText(),
            "road_type": self.road_type.currentText(),
            "paved_road": self.paved_road.isChecked(),
        }
