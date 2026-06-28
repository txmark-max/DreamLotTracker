from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLineEdit,
    QVBoxLayout,
)

from dreamlottracker.database.models import Listing, Property, ScoreComponent


class PropertyDialog(QDialog):
    def __init__(self, parent=None, property_: Property | None = None):
        super().__init__(parent)

        self.setWindowTitle("Edit Property" if property_ else "Add Property")
        self.property_ = property_

        self.address = QLineEdit()
        self.city = QLineEdit()

        self.price = QDoubleSpinBox()
        self.price.setMaximum(10_000_000)
        self.price.setPrefix("$")
        self.price.setDecimals(0)

        self.acres = QDoubleSpinBox()
        self.acres.setMaximum(1000)
        self.acres.setDecimals(2)

        self.score = QDoubleSpinBox()
        self.score.setMaximum(100)
        self.score.setDecimals(0)

        self.status = QComboBox()
        self.status.addItems(["Active", "Pending", "Sold", "Watch", "Off Market"])

        if property_:
            listing = property_.listings[0] if property_.listings else None
            scores = property_.scores

            self.address.setText(property_.address)
            self.city.setText(property_.city)
            self.acres.setValue(property_.acres or 0)
            self.price.setValue(listing.asking_price if listing else 0)
            self.score.setValue(scores.dream_score if scores and scores.dream_score else 0)
            self.status.setCurrentText(listing.status if listing else "Active")

        form = QFormLayout()
        form.addRow("Address", self.address)
        form.addRow("City", self.city)
        form.addRow("Asking Price", self.price)
        form.addRow("Acres", self.acres)
        form.addRow("Dream Score", self.score)
        form.addRow("Status", self.status)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_property(self) -> Property:
        prop = Property(
            address=self.address.text().strip(),
            city=self.city.text().strip(),
            county="Baldwin",
            state="AL",
            acres=float(self.acres.value()),
        )

        prop.listings.append(
            Listing(
                source="Manual",
                status=self.status.currentText(),
                asking_price=float(self.price.value()),
            )
        )

        prop.scores = ScoreComponent(
            dream_score=float(self.score.value()),
        )

        return prop
