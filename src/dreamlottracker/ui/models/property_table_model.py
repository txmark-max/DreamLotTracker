from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt


class PropertyTableModel(QAbstractTableModel):
    headers = [
        "Address",
        "City",
        "Price",
        "Acres",
        "Price/Acre",
        "Dream Score",
        "Price",
        "Location",
        "Utilities",
        "Flood",
        "Restrictions",
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
        acres = prop.acres or 0
        price_per_acre = price / acres if acres else 0
        status = listing.status if listing else "Unknown"

        dream_score = scores.dream_score if scores and scores.dream_score is not None else 0
        price_score = scores.price_score if scores and scores.price_score is not None else 0
        location_score = scores.location_score if scores and scores.location_score is not None else 0
        utilities_score = scores.utilities_score if scores and scores.utilities_score is not None else 0
        flood_score = scores.flood_score if scores and scores.flood_score is not None else 0
        restrictions_score = scores.restrictions_score if scores and scores.restrictions_score is not None else 0
        recommendation = scores.recommendation if scores and scores.recommendation else ""

        display_values = [
            prop.address,
            prop.city,
            f"${price:,.0f}",
            f"{acres:.2f}",
            f"${price_per_acre:,.0f}",
            f"{dream_score:.1f}",
            f"{price_score:.1f}",
            f"{location_score:.1f}",
            f"{utilities_score:.1f}",
            f"{flood_score:.1f}",
            f"{restrictions_score:.1f}",
            status,
            recommendation,
        ]

        sort_values = [
            prop.address,
            prop.city,
            price,
            acres,
            price_per_acre,
            dream_score,
            price_score,
            location_score,
            utilities_score,
            flood_score,
            restrictions_score,
            status,
            recommendation,
        ]

        if role == Qt.DisplayRole:
            return display_values[column]

        if role == Qt.UserRole:
            return sort_values[column]

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
