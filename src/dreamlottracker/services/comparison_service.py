from dreamlottracker.database.models import Property
from dreamlottracker.services.property_service import PropertyService


class ComparisonService:
    def __init__(self):
        self.property_service = PropertyService()

    def get_properties(self) -> list[Property]:
        return self.property_service.get_all_properties()

    def build_comparison_rows(self, properties: list[Property]) -> list[tuple[str, list[str]]]:
        rows = [
            ("City", []),
            ("Price", []),
            ("Acres", []),
            ("Price / Acre", []),
            ("Status", []),
            ("Dream Score", []),
            ("Recommendation", []),
        ]

        for property_ in properties:
            listing = property_.listings[0] if property_.listings else None
            scores = property_.scores

            price = float(listing.asking_price) if listing else 0.0
            acres = float(property_.acres or 0)
            price_per_acre = price / acres if acres > 0 else 0
            status = listing.status if listing else "Unknown"
            dream_score = float(scores.dream_score) if scores and scores.dream_score is not None else 0.0
            recommendation = scores.recommendation if scores and scores.recommendation else ""

            values = [
                property_.city or "",
                f"${price:,.0f}",
                f"{acres:.2f}",
                f"${price_per_acre:,.0f}",
                status,
                f"{dream_score:.1f}",
                recommendation,
            ]

            for row_index, value in enumerate(values):
                rows[row_index][1].append(value)

        return rows
