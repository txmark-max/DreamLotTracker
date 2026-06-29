from PySide6.QtWidgets import QFormLayout, QWidget

from dreamlottracker.ui.property_workspace.form_helpers import money


class FinancialTab(QWidget):
    def __init__(self, property_):
        super().__init__()
        fin = property_.financials

        form = QFormLayout()

        self.estimated_market_value = money(fin.estimated_market_value if fin and fin.estimated_market_value else 0)
        self.recommended_offer = money(fin.recommended_offer if fin and fin.recommended_offer else 0)
        self.maximum_offer = money(fin.maximum_offer if fin and fin.maximum_offer else 0)
        self.annual_taxes = money(fin.annual_taxes if fin and fin.annual_taxes else 0)
        self.estimated_site_prep = money(fin.estimated_site_prep if fin and fin.estimated_site_prep else 0)
        self.estimated_clearing = money(fin.estimated_clearing if fin and fin.estimated_clearing else 0)
        self.estimated_driveway = money(fin.estimated_driveway if fin and fin.estimated_driveway else 0)
        self.estimated_septic = money(fin.estimated_septic if fin and fin.estimated_septic else 0)
        self.estimated_utilities = money(fin.estimated_utilities if fin and fin.estimated_utilities else 0)

        form.addRow("Estimated Market Value", self.estimated_market_value)
        form.addRow("Recommended Offer", self.recommended_offer)
        form.addRow("Maximum Offer", self.maximum_offer)
        form.addRow("Annual Taxes", self.annual_taxes)
        form.addRow("Estimated Site Prep", self.estimated_site_prep)
        form.addRow("Estimated Clearing", self.estimated_clearing)
        form.addRow("Estimated Driveway", self.estimated_driveway)
        form.addRow("Estimated Septic", self.estimated_septic)
        form.addRow("Estimated Utilities", self.estimated_utilities)

        self.setLayout(form)

    def values(self):
        return {
            "estimated_market_value": float(self.estimated_market_value.value()),
            "recommended_offer": float(self.recommended_offer.value()),
            "maximum_offer": float(self.maximum_offer.value()),
            "annual_taxes": float(self.annual_taxes.value()),
            "estimated_site_prep": float(self.estimated_site_prep.value()),
            "estimated_clearing": float(self.estimated_clearing.value()),
            "estimated_driveway": float(self.estimated_driveway.value()),
            "estimated_septic": float(self.estimated_septic.value()),
            "estimated_utilities": float(self.estimated_utilities.value()),
        }
