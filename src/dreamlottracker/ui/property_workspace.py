from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QDialog, QDialogButtonBox, QDoubleSpinBox,
    QFormLayout, QLabel, QLineEdit, QMessageBox, QPlainTextEdit,
    QTableWidget, QTableWidgetItem, QTabWidget, QVBoxLayout, QWidget,
)

from dreamlottracker.services.property_service import PropertyService


class PropertyWorkspace(QDialog):
    def __init__(self, property_id: int, parent=None):
        super().__init__(parent)
        self.property_id = property_id
        self.service = PropertyService()
        self.property_ = self.service.get_property(property_id)

        if not self.property_:
            QMessageBox.warning(self, "Property Not Found", "Property could not be loaded.")
            self.reject()
            return

        self.setWindowTitle(f"Property Workspace - {self.property_.address}")
        self.resize(900, 700)

        layout = QVBoxLayout()
        title = QLabel(self.property_.address)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        tabs = QTabWidget()
        tabs.addTab(self._overview_tab(), "Overview")
        tabs.addTab(self._listing_tab(), "Listing")
        tabs.addTab(self._utilities_tab(), "Utilities")
        tabs.addTab(self._restrictions_tab(), "Restrictions")
        tabs.addTab(self._scores_tab(), "Scores")
        tabs.addTab(self._price_history_tab(), "Price History")
        tabs.addTab(self._notes_tab(), "Notes")

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Close)
        buttons.accepted.connect(self.save)
        buttons.rejected.connect(self.reject)

        layout.addWidget(title)
        layout.addWidget(tabs)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def _overview_tab(self):
        widget = QWidget()
        form = QFormLayout()
        self.address = QLineEdit(self.property_.address or "")
        self.city = QLineEdit(self.property_.city or "")
        self.county = QLineEdit(self.property_.county or "")
        self.state = QLineEdit(self.property_.state or "")
        self.zip_code = QLineEdit(self.property_.zip_code or "")
        self.parcel_number = QLineEdit(self.property_.parcel_number or "")
        self.acres = QDoubleSpinBox(); self.acres.setMaximum(10000); self.acres.setDecimals(2); self.acres.setValue(float(self.property_.acres or 0))
        self.latitude = QDoubleSpinBox(); self.latitude.setRange(-90, 90); self.latitude.setDecimals(6); self.latitude.setValue(float(self.property_.latitude or 0))
        self.longitude = QDoubleSpinBox(); self.longitude.setRange(-180, 180); self.longitude.setDecimals(6); self.longitude.setValue(float(self.property_.longitude or 0))
        for label, field in [("Address", self.address), ("City", self.city), ("County", self.county), ("State", self.state), ("ZIP", self.zip_code), ("Parcel Number", self.parcel_number), ("Acres", self.acres), ("Latitude", self.latitude), ("Longitude", self.longitude)]:
            form.addRow(label, field)
        widget.setLayout(form)
        return widget

    def _listing_tab(self):
        widget = QWidget()
        form = QFormLayout()
        listing = self.property_.listings[0] if self.property_.listings else None
        self.asking_price = QDoubleSpinBox(); self.asking_price.setMaximum(100000000); self.asking_price.setPrefix("$"); self.asking_price.setDecimals(0); self.asking_price.setValue(float(listing.asking_price if listing else 0))
        self.status = QComboBox(); self.status.addItems(["Active", "Pending", "Sold", "Watch", "Off Market"]); self.status.setCurrentText(listing.status if listing else "Active")
        form.addRow("Asking Price", self.asking_price); form.addRow("Status", self.status)
        widget.setLayout(form)
        return widget

    def _utilities_tab(self):
        widget = QWidget()
        form = QFormLayout()
        utilities = self.property_.utilities
        self.electric = self._combo(["Unknown", "At Road", "Available", "Nearby", "Unavailable"], utilities.electric if utilities and utilities.electric else "Unknown")
        self.county_water = self._combo(["Unknown", "Available", "Unavailable"], utilities.county_water if utilities and utilities.county_water else "Unknown")
        self.public_sewer = self._combo(["Unknown", "Available", "Unavailable"], utilities.public_sewer if utilities and utilities.public_sewer else "Unknown")
        self.septic_required = QCheckBox(); self.septic_required.setChecked(bool(utilities.septic_required) if utilities and utilities.septic_required is not None else False)
        self.fiber = self._combo(["Unknown", "Available", "Planned", "Unavailable"], utilities.fiber if utilities and utilities.fiber else "Unknown")
        self.natural_gas = self._combo(["Unknown", "Available", "Unavailable"], utilities.natural_gas if utilities and utilities.natural_gas else "Unknown")
        self.utility_notes = QPlainTextEdit(utilities.notes if utilities and utilities.notes else "")
        for label, field in [("Electric", self.electric), ("County Water", self.county_water), ("Public Sewer", self.public_sewer), ("Septic Required", self.septic_required), ("Fiber", self.fiber), ("Natural Gas", self.natural_gas), ("Utility Notes", self.utility_notes)]:
            form.addRow(label, field)
        widget.setLayout(form)
        return widget

    def _restrictions_tab(self):
        widget = QWidget()
        form = QFormLayout()
        restrictions = self.property_.restrictions
        self.hoa = self._combo(["Unknown", "None", "No", "Yes"], restrictions.hoa if restrictions and restrictions.hoa else "Unknown")
        self.hoa_fee = QDoubleSpinBox(); self.hoa_fee.setMaximum(100000); self.hoa_fee.setPrefix("$"); self.hoa_fee.setDecimals(0); self.hoa_fee.setValue(float(restrictions.hoa_fee if restrictions and restrictions.hoa_fee else 0))
        self.shop_allowed = self._check(restrictions.shop_allowed if restrictions else None)
        self.rv_allowed = self._check(restrictions.rv_allowed if restrictions else None)
        self.boat_allowed = self._check(restrictions.boat_allowed if restrictions else None)
        self.livestock_allowed = self._check(restrictions.livestock_allowed if restrictions else None)
        self.mobile_home_allowed = self._check(restrictions.mobile_home_allowed if restrictions else None)
        self.barndominium_allowed = self._check(restrictions.barndominium_allowed if restrictions else None)
        self.restriction_notes = QPlainTextEdit(restrictions.notes if restrictions and restrictions.notes else "")
        for label, field in [("HOA", self.hoa), ("HOA Fee", self.hoa_fee), ("Shop Allowed", self.shop_allowed), ("RV Allowed", self.rv_allowed), ("Boat Allowed", self.boat_allowed), ("Livestock Allowed", self.livestock_allowed), ("Mobile Homes Allowed", self.mobile_home_allowed), ("Barndominium Allowed", self.barndominium_allowed), ("Restriction Notes", self.restriction_notes)]:
            form.addRow(label, field)
        widget.setLayout(form)
        return widget

    def _scores_tab(self):
        widget = QWidget()
        form = QFormLayout()
        scores = self.property_.scores
        self.dream_score = QDoubleSpinBox(); self.dream_score.setMaximum(100); self.dream_score.setDecimals(1); self.dream_score.setValue(float(scores.dream_score if scores and scores.dream_score else 0))
        self.recommendation = self._combo(["Dream Lot", "Strong Buy", "Watch List", "Pass"], scores.recommendation if scores and scores.recommendation else "Watch List")
        form.addRow("Dream Score", self.dream_score); form.addRow("Recommendation", self.recommendation)
        widget.setLayout(form)
        return widget

    def _price_history_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        listing = self.property_.listings[0] if self.property_.listings else None
        history = sorted(listing.price_history if listing else [], key=lambda item: item.recorded_date, reverse=True)
        table = QTableWidget(len(history), 3)
        table.setHorizontalHeaderLabels(["Date", "Price", "Note"])
        for row, entry in enumerate(history):
            table.setItem(row, 0, QTableWidgetItem(entry.recorded_date.strftime("%Y-%m-%d")))
            table.setItem(row, 1, QTableWidgetItem(f"${entry.price:,.0f}"))
            table.setItem(row, 2, QTableWidgetItem(entry.note or ""))
        table.resizeColumnsToContents()
        layout.addWidget(table)
        widget.setLayout(layout)
        return widget

    def _notes_tab(self):
        widget = QWidget()
        form = QFormLayout()
        note = self.property_.notes[0] if self.property_.notes else None
        self.pros = QPlainTextEdit(note.pros if note and note.pros else "")
        self.cons = QPlainTextEdit(note.cons if note and note.cons else "")
        self.questions = QPlainTextEdit(note.questions if note and note.questions else "")
        self.builder_notes = QPlainTextEdit(note.builder_notes if note and note.builder_notes else "")
        self.final_recommendation = QPlainTextEdit(note.final_recommendation if note and note.final_recommendation else "")
        for label, field in [("Pros", self.pros), ("Cons", self.cons), ("Questions", self.questions), ("Builder Notes", self.builder_notes), ("Final Recommendation", self.final_recommendation)]:
            form.addRow(label, field)
        widget.setLayout(form)
        return widget

    def _combo(self, values, current):
        combo = QComboBox()
        combo.addItems(values)
        combo.setCurrentText(current)
        return combo

    def _check(self, value):
        check = QCheckBox()
        check.setChecked(bool(value) if value is not None else False)
        return check

    def save(self):
        self.service.update_property_workspace(
            property_id=self.property_id,
            address=self.address.text().strip(),
            city=self.city.text().strip(),
            county=self.county.text().strip(),
            state=self.state.text().strip(),
            zip_code=self.zip_code.text().strip(),
            parcel_number=self.parcel_number.text().strip(),
            acres=float(self.acres.value()),
            latitude=float(self.latitude.value()),
            longitude=float(self.longitude.value()),
            asking_price=float(self.asking_price.value()),
            status=self.status.currentText(),
            dream_score=float(self.dream_score.value()),
            recommendation=self.recommendation.currentText(),
            pros=self.pros.toPlainText(),
            cons=self.cons.toPlainText(),
            questions=self.questions.toPlainText(),
            builder_notes=self.builder_notes.toPlainText(),
            final_recommendation=self.final_recommendation.toPlainText(),
            electric=self.electric.currentText(),
            county_water=self.county_water.currentText(),
            public_sewer=self.public_sewer.currentText(),
            septic_required=self.septic_required.isChecked(),
            fiber=self.fiber.currentText(),
            natural_gas=self.natural_gas.currentText(),
            utility_notes=self.utility_notes.toPlainText(),
            hoa=self.hoa.currentText(),
            hoa_fee=float(self.hoa_fee.value()),
            shop_allowed=self.shop_allowed.isChecked(),
            rv_allowed=self.rv_allowed.isChecked(),
            boat_allowed=self.boat_allowed.isChecked(),
            livestock_allowed=self.livestock_allowed.isChecked(),
            mobile_home_allowed=self.mobile_home_allowed.isChecked(),
            barndominium_allowed=self.barndominium_allowed.isChecked(),
            restriction_notes=self.restriction_notes.toPlainText(),
        )
        self.service.recalculate_scores()
        QMessageBox.information(self, "Saved", "Property workspace saved.")
        self.accept()
