from pathlib import Path

from PySide6.QtWidgets import QFileDialog, QHBoxLayout, QListWidget, QListWidgetItem, QMessageBox, QPushButton, QVBoxLayout, QWidget

from dreamlottracker.services.file_service import FileService


class DocumentsTab(QWidget):
    def __init__(self, property_):
        super().__init__()
        self.property_ = property_
        self.file_service = FileService()

        layout = QVBoxLayout()
        self.document_list = QListWidget()

        for document in property_.documents:
            item = QListWidgetItem(f"{Path(document.file_path).name} — {document.document_type or ''} — {document.notes or ''}")
            item.setData(1000, document.id)
            item.setData(1001, document.file_path)
            self.document_list.addItem(item)

        buttons = QHBoxLayout()
        add_button = QPushButton("Add Document")
        add_button.clicked.connect(self.add_document)
        open_button = QPushButton("Open Selected")
        open_button.clicked.connect(self.open_selected)
        delete_button = QPushButton("Remove Selected")
        delete_button.clicked.connect(self.delete_selected)

        buttons.addWidget(add_button)
        buttons.addWidget(open_button)
        buttons.addWidget(delete_button)

        layout.addWidget(self.document_list)
        layout.addLayout(buttons)
        self.setLayout(layout)

    def add_document(self):
        path_text, _ = QFileDialog.getOpenFileName(
            self,
            "Add Document",
            "",
            "Documents (*.pdf *.docx *.xlsx *.png *.jpg *.jpeg);;All Files (*)",
        )
        if path_text:
            self.file_service.add_document(self.property_.id, Path(path_text))
            QMessageBox.information(self, "Document Added", "Document added. Reopen workspace to refresh the list.")

    def open_selected(self):
        selected = self.document_list.selectedItems()
        if selected:
            self.file_service.open_file(selected[0].data(1001))

    def delete_selected(self):
        selected = self.document_list.selectedItems()
        if selected:
            self.file_service.delete_document(selected[0].data(1000))
            QMessageBox.information(self, "Removed", "Document reference removed. Reopen workspace to refresh.")
