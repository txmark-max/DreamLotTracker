from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt


class PropertyTableModel(QAbstractTableModel):
    headers = [
        "Address",
        "City",
        "Price",
        "Acres",
        "Dream Score",
        "Status",
        "Recommendation",
    ]

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

        listing = prop.listings[0] if prop.listings else None
        scores = prop.scores

        price = listing.asking_price if listing else 0
        status = listing.status if listing else "Unknown"
        dream_score = scores.dream_score if scores and scores.dream_score is not None else 0
        recommendation = scores.recommendation if scores and scores.recommendation else ""

        if role == Qt.DisplayRole:
            if column == 0:
                return prop.address
            if column == 1:
                return prop.city
            if column == 2:
                return f"${price:,.0f}"
            if column == 3:
                return f"{prop.acres:.2f}"
            if column == 4:
                return f"{dream_score:.1f}"
            if column == 5:
                return status
            if column == 6:
                return recommendation

        if role == Qt.UserRole:
            if column == 2:
                return price
            if column == 3:
                return prop.acres
            if column == 4:
                return dream_score

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
