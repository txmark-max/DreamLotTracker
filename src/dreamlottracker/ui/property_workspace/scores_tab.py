from PySide6.QtWidgets import QFormLayout, QLabel, QWidget

from dreamlottracker.ui.property_workspace.form_helpers import combo, double


class ScoresTab(QWidget):
    def __init__(self, property_):
        super().__init__()
        scores = property_.scores

        form = QFormLayout()

        self.dream_score = double(100, 1, scores.dream_score if scores and scores.dream_score else 0)
        self.recommendation = combo(
            ["Dream Lot", "Strong Buy", "Watch List", "Pass"],
            scores.recommendation if scores and scores.recommendation else "Watch List",
        )

        form.addRow("Dream Score", self.dream_score)
        form.addRow("Recommendation", self.recommendation)

        if scores:
            form.addRow("Price Score", QLabel(f"{scores.price_score or 0:.1f}"))
            form.addRow("Location Score", QLabel(f"{scores.location_score or 0:.1f}"))
            form.addRow("Utilities Score", QLabel(f"{scores.utilities_score or 0:.1f}"))
            form.addRow("Flood Score", QLabel(f"{scores.flood_score or 0:.1f}"))
            form.addRow("Restrictions Score", QLabel(f"{scores.restrictions_score or 0:.1f}"))

        self.setLayout(form)

    def values(self):
        return {
            "dream_score": float(self.dream_score.value()),
            "recommendation": self.recommendation.currentText(),
        }
