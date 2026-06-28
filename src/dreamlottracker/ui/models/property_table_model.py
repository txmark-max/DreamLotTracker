from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt


class PropertyTableModel(QAbstractTableModel):
    headers = ["Address", "City", "Price", "Acres", "Dream Score", "Status"]

    def __init__(self, properties=None):
        super().__init__()
        self.properties = properties or []

    def rowCount(self, parent=QModelIndex()):
        return len(self.properties)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        prop = self.properties[index.row()]
        column = index.column()

        if role == Qt.DisplayRole:
            if column == 0:
                return prop.address
            if column == 1:
                return prop.city
            if column == 2:
                return f"${prop.asking_price:,.0f}"
            if column == 3:
                return f"{prop.acres:.2f}"
            if column == 4:
                return f"{prop.dream_score:.0f}"
            if column == 5:
                return prop.status

        if role == Qt.UserRole:
            if column == 2:
                return prop.asking_price
            if column == 3:
                return prop.acres
            if column == 4:
                return prop.dream_score

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]
        return None

    def set_properties(self, properties):
        self.beginResetModel()
        self.properties = properties
        self.endResetModel()

    def property_at(self, row: int):
        if 0 <= row < len(self.properties):
            return self.properties[row]
        return None
