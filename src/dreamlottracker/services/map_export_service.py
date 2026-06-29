from pathlib import Path

import simplekml

from dreamlottracker.services.property_service import PropertyService


class MapExportService:
    def __init__(self):
        self.property_service = PropertyService()

    def export_kml(self, output_path: Path) -> Path:
        properties = self.property_service.get_all_properties()

        output_path.parent.mkdir(parents=True, exist_ok=True)

        kml = simplekml.Kml()
        kml.document.name = "Dream Lot Tracker Properties"

        for property_ in properties:
            if property_.latitude is None or property_.longitude is None:
                continue

            listing = property_.listings[0] if property_.listings else None
            scores = property_.scores

            price = listing.asking_price if listing else 0
            status = listing.status if listing else "Unknown"
            dream_score = scores.dream_score if scores and scores.dream_score is not None else 0
            recommendation = scores.recommendation if scores and scores.recommendation else ""

            point = kml.newpoint(
                name=f"{property_.address} ({dream_score:.1f})",
                coords=[(property_.longitude, property_.latitude)],
            )

            point.description = (
                f"Address: {property_.address}<br>"
                f"City: {property_.city}<br>"
                f"Price: ${price:,.0f}<br>"
                f"Acres: {property_.acres:.2f}<br>"
                f"Status: {status}<br>"
                f"Dream Score: {dream_score:.1f}<br>"
                f"Recommendation: {recommendation}"
            )

            if dream_score >= 95:
                point.style.iconstyle.color = simplekml.Color.green
            elif dream_score >= 85:
                point.style.iconstyle.color = simplekml.Color.yellow
            else:
                point.style.iconstyle.color = simplekml.Color.red

        kml.save(str(output_path))
        return output_path
