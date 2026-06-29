from PySide6.QtWidgets import QFormLayout, QLineEdit, QWidget

from dreamlottracker.ui.property_workspace.form_helpers import double


class OverviewTab(QWidget):
    def __init__(self, property_):
        super().__init__()
        self.property_ = property_

        form = QFormLayout()

        self.address = QLineEdit(property_.address or "")
        self.city = QLineEdit(property_.city or "")
        self.county = QLineEdit(property_.county or "")
        self.state = QLineEdit(property_.state or "")
        self.zip_code = QLineEdit(property_.zip_code or "")
        self.parcel_number = QLineEdit(property_.parcel_number or "")
        self.acres = double(10000, 2, property_.acres or 0)
        self.latitude = double(90, 6, property_.latitude or 0, minimum=-90)
        self.longitude = double(180, 6, property_.longitude or 0, minimum=-180)

        form.addRow("Address", self.address)
        form.addRow("City", self.city)
        form.addRow("County", self.county)
        form.addRow("State", self.state)
        form.addRow("ZIP", self.zip_code)
        form.addRow("Parcel Number", self.parcel_number)
        form.addRow("Acres", self.acres)
        form.addRow("Latitude", self.latitude)
        form.addRow("Longitude", self.longitude)

        self.setLayout(form)

    def values(self):
        return {
            "address": self.address.text().strip(),
            "city": self.city.text().strip(),
            "county": self.county.text().strip(),
            "state": self.state.text().strip(),
            "zip_code": self.zip_code.text().strip(),
            "parcel_number": self.parcel_number.text().strip(),
            "acres": float(self.acres.value()),
            "latitude": float(self.latitude.value()),
            "longitude": float(self.longitude.value()),
        }
