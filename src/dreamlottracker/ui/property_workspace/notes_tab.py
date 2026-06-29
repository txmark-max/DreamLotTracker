from PySide6.QtWidgets import QFormLayout, QPlainTextEdit, QWidget


class NotesTab(QWidget):
    def __init__(self, property_):
        super().__init__()
        note = property_.notes[0] if property_.notes else None

        form = QFormLayout()

        self.pros = QPlainTextEdit(note.pros if note and note.pros else "")
        self.cons = QPlainTextEdit(note.cons if note and note.cons else "")
        self.questions = QPlainTextEdit(note.questions if note and note.questions else "")
        self.builder_notes = QPlainTextEdit(note.builder_notes if note and note.builder_notes else "")
        self.final_recommendation = QPlainTextEdit(note.final_recommendation if note and note.final_recommendation else "")

        form.addRow("Pros", self.pros)
        form.addRow("Cons", self.cons)
        form.addRow("Questions", self.questions)
        form.addRow("Builder Notes", self.builder_notes)
        form.addRow("Final Recommendation", self.final_recommendation)

        self.setLayout(form)

    def values(self):
        return {
            "pros": self.pros.toPlainText(),
            "cons": self.cons.toPlainText(),
            "questions": self.questions.toPlainText(),
            "builder_notes": self.builder_notes.toPlainText(),
            "final_recommendation": self.final_recommendation.toPlainText(),
        }
