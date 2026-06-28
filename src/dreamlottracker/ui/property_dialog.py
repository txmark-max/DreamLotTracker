from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLineEdit,
    QVBoxLayout,
)

from dreamlottracker.database.models import Property


class PropertyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add Property")

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

        form = QFormLayout()
        form.addRow("Address", self.address)
        form.addRow("City", self.city)
        form.addRow("Asking Price", self.price)
        form.addRow("Acres", self.acres)
        form.addRow("Dream Score", self.score)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_property(self) -> Property:
        return Property(
            address=self.address.text().strip(),
            city=self.city.text().strip(),
            asking_price=float(self.price.value()),
            acres=float(self.acres.value()),
            dream_score=float(self.score.value()),
            status="Active",
        )
