from PySide6.QtWidgets import QFormLayout, QPlainTextEdit, QWidget

from dreamlottracker.ui.property_workspace.form_helpers import check, combo, money


class RestrictionsTab(QWidget):
    def __init__(self, property_):
        super().__init__()
        restrictions = property_.restrictions

        form = QFormLayout()

        self.hoa = combo(["Unknown", "None", "No", "Yes"], restrictions.hoa if restrictions and restrictions.hoa else "Unknown")
        self.hoa_fee = money(restrictions.hoa_fee if restrictions and restrictions.hoa_fee else 0)
        self.shop_allowed = check(restrictions.shop_allowed if restrictions else None)
        self.rv_allowed = check(restrictions.rv_allowed if restrictions else None)
        self.boat_allowed = check(restrictions.boat_allowed if restrictions else None)
        self.livestock_allowed = check(restrictions.livestock_allowed if restrictions else None)
        self.mobile_home_allowed = check(restrictions.mobile_home_allowed if restrictions else None)
        self.barndominium_allowed = check(restrictions.barndominium_allowed if restrictions else None)
        self.restriction_notes = QPlainTextEdit(restrictions.notes if restrictions and restrictions.notes else "")

        form.addRow("HOA", self.hoa)
        form.addRow("HOA Fee", self.hoa_fee)
        form.addRow("Shop Allowed", self.shop_allowed)
        form.addRow("RV Allowed", self.rv_allowed)
        form.addRow("Boat Allowed", self.boat_allowed)
        form.addRow("Livestock Allowed", self.livestock_allowed)
        form.addRow("Mobile Homes Allowed", self.mobile_home_allowed)
        form.addRow("Barndominium Allowed", self.barndominium_allowed)
        form.addRow("Restriction Notes", self.restriction_notes)

        self.setLayout(form)

    def values(self):
        return {
            "hoa": self.hoa.currentText(),
            "hoa_fee": float(self.hoa_fee.value()),
            "shop_allowed": self.shop_allowed.isChecked(),
            "rv_allowed": self.rv_allowed.isChecked(),
            "boat_allowed": self.boat_allowed.isChecked(),
            "livestock_allowed": self.livestock_allowed.isChecked(),
            "mobile_home_allowed": self.mobile_home_allowed.isChecked(),
            "barndominium_allowed": self.barndominium_allowed.isChecked(),
            "restriction_notes": self.restriction_notes.toPlainText(),
        }
