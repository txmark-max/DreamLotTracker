from PySide6.QtWidgets import QFormLayout, QPlainTextEdit, QWidget

from dreamlottracker.ui.property_workspace.form_helpers import check, combo


class UtilitiesTab(QWidget):
    def __init__(self, property_):
        super().__init__()
        utilities = property_.utilities

        form = QFormLayout()

        self.electric = combo(["Unknown", "At Road", "Available", "Nearby", "Unavailable"], utilities.electric if utilities and utilities.electric else "Unknown")
        self.county_water = combo(["Unknown", "Available", "Unavailable"], utilities.county_water if utilities and utilities.county_water else "Unknown")
        self.public_sewer = combo(["Unknown", "Available", "Unavailable"], utilities.public_sewer if utilities and utilities.public_sewer else "Unknown")
        self.septic_required = check(utilities.septic_required if utilities else None)
        self.fiber = combo(["Unknown", "Available", "Planned", "Unavailable"], utilities.fiber if utilities and utilities.fiber else "Unknown")
        self.natural_gas = combo(["Unknown", "Available", "Unavailable"], utilities.natural_gas if utilities and utilities.natural_gas else "Unknown")
        self.utility_notes = QPlainTextEdit(utilities.notes if utilities and utilities.notes else "")

        form.addRow("Electric", self.electric)
        form.addRow("County Water", self.county_water)
        form.addRow("Public Sewer", self.public_sewer)
        form.addRow("Septic Required", self.septic_required)
        form.addRow("Fiber", self.fiber)
        form.addRow("Natural Gas", self.natural_gas)
        form.addRow("Utility Notes", self.utility_notes)

        self.setLayout(form)

    def values(self):
        return {
            "electric": self.electric.currentText(),
            "county_water": self.county_water.currentText(),
            "public_sewer": self.public_sewer.currentText(),
            "septic_required": self.septic_required.isChecked(),
            "fiber": self.fiber.currentText(),
            "natural_gas": self.natural_gas.currentText(),
            "utility_notes": self.utility_notes.toPlainText(),
        }
