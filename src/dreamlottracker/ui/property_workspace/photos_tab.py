from pathlib import Path

from PySide6.QtWidgets import QFileDialog, QHBoxLayout, QListWidget, QListWidgetItem, QMessageBox, QPushButton, QVBoxLayout, QWidget

from dreamlottracker.services.file_service import FileService


class PhotosTab(QWidget):
    def __init__(self, property_):
        super().__init__()
        self.property_ = property_
        self.file_service = FileService()

        layout = QVBoxLayout()
        self.photo_list = QListWidget()

        for photo in property_.photos:
            item = QListWidgetItem(f"{Path(photo.file_path).name} — {photo.photo_type or ''} — {photo.caption or ''}")
            item.setData(1000, photo.id)
            item.setData(1001, photo.file_path)
            self.photo_list.addItem(item)

        buttons = QHBoxLayout()
        add_button = QPushButton("Add Photo")
        add_button.clicked.connect(self.add_photo)
        open_button = QPushButton("Open Selected")
        open_button.clicked.connect(self.open_selected)
        delete_button = QPushButton("Remove Selected")
        delete_button.clicked.connect(self.delete_selected)

        buttons.addWidget(add_button)
        buttons.addWidget(open_button)
        buttons.addWidget(delete_button)

        layout.addWidget(self.photo_list)
        layout.addLayout(buttons)
        self.setLayout(layout)

    def add_photo(self):
        path_text, _ = QFileDialog.getOpenFileName(
            self,
            "Add Photo",
            "",
            "Images (*.png *.jpg *.jpeg *.webp *.heic);;All Files (*)",
        )
        if path_text:
            self.file_service.add_photo(self.property_.id, Path(path_text))
            QMessageBox.information(self, "Photo Added", "Photo added. Reopen workspace to refresh the list.")

    def open_selected(self):
        selected = self.photo_list.selectedItems()
        if selected:
            self.file_service.open_file(selected[0].data(1001))

    def delete_selected(self):
        selected = self.photo_list.selectedItems()
        if selected:
            self.file_service.delete_photo(selected[0].data(1000))
            QMessageBox.information(self, "Removed", "Photo reference removed. Reopen workspace to refresh.")
