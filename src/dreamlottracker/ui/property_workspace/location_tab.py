from PySide6.QtWidgets import QFormLayout, QLabel, QWidget

from dreamlottracker.ui.property_workspace.form_helpers import check, combo, spin


class LocationTab(QWidget):
    def __init__(self, property_):
        super().__init__()
        loc = property_.location_metrics

        form = QFormLayout()

        self.minutes_to_gulf_shores = spin(loc.minutes_to_gulf_shores if loc and loc.minutes_to_gulf_shores else 0)
        self.minutes_to_foley = spin(loc.minutes_to_foley if loc and loc.minutes_to_foley else 0)
        self.minutes_to_fairhope = spin(loc.minutes_to_fairhope if loc and loc.minutes_to_fairhope else 0)
        self.minutes_to_pensacola = spin(loc.minutes_to_pensacola if loc and loc.minutes_to_pensacola else 0)
        self.flood_zone = combo(["Unknown", "X", "AE", "VE"], loc.flood_zone if loc and loc.flood_zone else "Unknown")
        self.wetlands = combo(["Unknown", "None", "Possible", "Confirmed"], loc.wetlands if loc and loc.wetlands else "Unknown")
        self.road_type = combo(["Unknown", "County", "Private", "State"], loc.road_type if loc and loc.road_type else "Unknown")
        self.paved_road = check(loc.paved_road if loc else None)

        form.addRow("Minutes to Gulf Shores", self.minutes_to_gulf_shores)
        form.addRow("Minutes to Foley", self.minutes_to_foley)
        form.addRow("Minutes to Fairhope", self.minutes_to_fairhope)
        form.addRow("Minutes to Pensacola", self.minutes_to_pensacola)
        form.addRow("Flood Zone", self.flood_zone)
        form.addRow("Wetlands", self.wetlands)
        form.addRow("Road Type", self.road_type)
        form.addRow("Paved Road", self.paved_road)

        note = QLabel(
            "Drive time is used for scoring. GPS coordinates remain on the Overview tab "
            "for future automatic lookups."
        )
        note.setWordWrap(True)
        note.setMinimumHeight(70)
        note.setStyleSheet("color: gray; font-style: italic;")
        form.addRow("", note)

        self.setLayout(form)

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
