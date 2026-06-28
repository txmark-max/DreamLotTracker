from PySide6.QtCore import Qt, QSortFilterProxyModel
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from dreamlottracker.repositories.property_repository import PropertyRepository
from dreamlottracker.ui.models.property_table_model import PropertyTableModel
from dreamlottracker.ui.property_dialog import PropertyDialog


class PropertiesPage(QWidget):
    def __init__(self):
        super().__init__()

        self.repository = PropertyRepository()

        layout = QVBoxLayout()
        header_layout = QHBoxLayout()

        title = QLabel("Properties")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search properties...")

        add_button = QPushButton("Add Property")
        add_button.clicked.connect(self.add_property)

        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(self.edit_selected_property)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_selected_property)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.search_box)
        header_layout.addWidget(add_button)
        header_layout.addWidget(edit_button)
        header_layout.addWidget(delete_button)

        self.table = QTableView()
        self.table.setSortingEnabled(True)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QTableView.SingleSelection)
        self.table.doubleClicked.connect(self.edit_selected_property)

        self.model = PropertyTableModel()
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy_model.setFilterKeyColumn(-1)

        self.table.setModel(self.proxy_model)

        layout.addLayout(header_layout)
        layout.addWidget(self.table)

        self.setLayout(layout)

        self.search_box.textChanged.connect(self.proxy_model.setFilterFixedString)

        self.load_properties()

    def load_properties(self):
        properties = self.repository.get_all()
        self.model.set_properties(properties)
        self.table.resizeColumnsToContents()

    def add_property(self):
        dialog = PropertyDialog(self)

        if dialog.exec():
            property_ = dialog.get_property()
            self.repository.add(property_)
            self.load_properties()

    def selected_property(self):
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            return None

        proxy_index = selected[0]
        source_index = self.proxy_model.mapToSource(proxy_index)
        return self.model.property_at(source_index.row())

    def edit_selected_property(self):
        prop = self.selected_property()
        if not prop:
            QMessageBox.information(self, "No Selection", "Please select a property to edit.")
            return

        dialog = PropertyDialog(self, prop)

        if dialog.exec():
            updated = dialog.get_property()
            self.repository.update(prop.id, updated)
            self.load_properties()

    def delete_selected_property(self):
        prop = self.selected_property()
        if not prop:
            QMessageBox.information(self, "No Selection", "Please select a property to delete.")
            return

        result = QMessageBox.question(
            self,
            "Delete Property",
            f"Delete {prop.address}?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if result == QMessageBox.Yes:
            self.repository.delete(prop.id)
            self.load_properties()
