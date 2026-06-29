from PySide6.QtWidgets import QFormLayout, QWidget

from dreamlottracker.ui.property_workspace.form_helpers import combo, money


class ListingTab(QWidget):
    def __init__(self, property_):
        super().__init__()
        listing = property_.listings[0] if property_.listings else None

        form = QFormLayout()

        self.asking_price = money(listing.asking_price if listing else 0)
        self.status = combo(
            ["Active", "Pending", "Sold", "Watch", "Off Market"],
            listing.status if listing else "Active",
        )

        form.addRow("Asking Price", self.asking_price)
        form.addRow("Status", self.status)
        self.setLayout(form)

    def values(self):
        return {
            "asking_price": float(self.asking_price.value()),
            "status": self.status.currentText(),
        }
