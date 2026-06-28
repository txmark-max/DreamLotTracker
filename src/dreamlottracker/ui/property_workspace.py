from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPlainTextEdit,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
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
        self.resize(850, 650)

        layout = QVBoxLayout()

        title = QLabel(self.property_.address)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        tabs = QTabWidget()
        tabs.addTab(self._overview_tab(), "Overview")
        tabs.addTab(self._listing_tab(), "Listing")
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

    def _overview_tab(self) -> QWidget:
        widget = QWidget()
        form = QFormLayout()

        self.address = QLineEdit(self.property_.address or "")
        self.city = QLineEdit(self.property_.city or "")
        self.county = QLineEdit(self.property_.county or "")
        self.state = QLineEdit(self.property_.state or "")
        self.zip_code = QLineEdit(self.property_.zip_code or "")
        self.parcel_number = QLineEdit(self.property_.parcel_number or "")

        self.acres = QDoubleSpinBox()
        self.acres.setMaximum(10_000)
        self.acres.setDecimals(2)
        self.acres.setValue(float(self.property_.acres or 0))

        form.addRow("Address", self.address)
        form.addRow("City", self.city)
        form.addRow("County", self.county)
        form.addRow("State", self.state)
        form.addRow("ZIP", self.zip_code)
        form.addRow("Parcel Number", self.parcel_number)
        form.addRow("Acres", self.acres)

        widget.setLayout(form)
        return widget

    def _listing_tab(self) -> QWidget:
        widget = QWidget()
        form = QFormLayout()

        listing = self.property_.listings[0] if self.property_.listings else None

        self.asking_price = QDoubleSpinBox()
        self.asking_price.setMaximum(100_000_000)
        self.asking_price.setPrefix("$")
        self.asking_price.setDecimals(0)
        self.asking_price.setValue(float(listing.asking_price if listing else 0))

        self.status = QComboBox()
        self.status.addItems(["Active", "Pending", "Sold", "Watch", "Off Market"])
        self.status.setCurrentText(listing.status if listing else "Active")

        form.addRow("Asking Price", self.asking_price)
        form.addRow("Status", self.status)

        widget.setLayout(form)
        return widget

    def _scores_tab(self) -> QWidget:
        widget = QWidget()
        form = QFormLayout()

        scores = self.property_.scores

        self.dream_score = QDoubleSpinBox()
        self.dream_score.setMaximum(100)
        self.dream_score.setDecimals(1)
        self.dream_score.setValue(float(scores.dream_score if scores and scores.dream_score else 0))

        self.recommendation = QComboBox()
        self.recommendation.addItems(["Dream Lot", "Strong Buy", "Watch List", "Pass"])
        self.recommendation.setCurrentText(
            scores.recommendation if scores and scores.recommendation else "Watch List"
        )

        form.addRow("Dream Score", self.dream_score)
        form.addRow("Recommendation", self.recommendation)

        widget.setLayout(form)
        return widget

    def _price_history_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()

        listing = self.property_.listings[0] if self.property_.listings else None
        history = listing.price_history if listing else []

        history = sorted(
            history,
            key=lambda item: item.recorded_date,
            reverse=True,
        )

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

    def _notes_tab(self) -> QWidget:
        widget = QWidget()
        form = QFormLayout()

        note = self.property_.notes[0] if self.property_.notes else None

        self.pros = QPlainTextEdit(note.pros if note and note.pros else "")
        self.cons = QPlainTextEdit(note.cons if note and note.cons else "")
        self.questions = QPlainTextEdit(note.questions if note and note.questions else "")
        self.builder_notes = QPlainTextEdit(note.builder_notes if note and note.builder_notes else "")
        self.final_recommendation = QPlainTextEdit(
            note.final_recommendation if note and note.final_recommendation else ""
        )

        form.addRow("Pros", self.pros)
        form.addRow("Cons", self.cons)
        form.addRow("Questions", self.questions)
        form.addRow("Builder Notes", self.builder_notes)
        form.addRow("Final Recommendation", self.final_recommendation)

        widget.setLayout(form)
        return widget

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
            asking_price=float(self.asking_price.value()),
            status=self.status.currentText(),
            dream_score=float(self.dream_score.value()),
            recommendation=self.recommendation.currentText(),
            pros=self.pros.toPlainText(),
            cons=self.cons.toPlainText(),
            questions=self.questions.toPlainText(),
            builder_notes=self.builder_notes.toPlainText(),
            final_recommendation=self.final_recommendation.toPlainText(),
        )

        QMessageBox.information(self, "Saved", "Property workspace saved.")
        self.accept()
