from dreamlottracker.database.models import Listing, Property, ScoreComponent
from dreamlottracker.repositories.property_repository import PropertyRepository


class PropertyService:
    def __init__(self):
        self.repository = PropertyRepository()

    def get_all_properties(self) -> list[Property]:
        return self.repository.get_all()

    def get_dashboard_stats(self) -> dict:
        return {
            "total": self.repository.count(),
            "active": self.repository.active_count(),
            "dream_lots": self.repository.dream_lot_count(),
            "average_score": self.repository.average_score(),
        }

    def add_property(
        self,
        address: str,
        city: str,
        acres: float,
        asking_price: float,
        dream_score: float,
        status: str = "Active",
    ) -> Property:
        prop = Property(
            address=address,
            city=city,
            county="Baldwin",
            state="AL",
            acres=acres,
        )

        prop.listings.append(
            Listing(
                source="Manual",
                status=status,
                asking_price=asking_price,
            )
        )

        prop.scores = ScoreComponent(
            dream_score=dream_score,
        )

        return self.repository.add(prop)

    def update_property(
        self,
        property_id: int,
        address: str,
        city: str,
        acres: float,
        asking_price: float,
        dream_score: float,
        status: str,
    ) -> None:
        updated = Property(
            address=address,
            city=city,
            county="Baldwin",
            state="AL",
            acres=acres,
        )

        updated.listings.append(
            Listing(
                source="Manual",
                status=status,
                asking_price=asking_price,
            )
        )

        updated.scores = ScoreComponent(
            dream_score=dream_score,
        )

        self.repository.update(property_id, updated)

    def delete_property(self, property_id: int) -> None:
        self.repository.delete(property_id)
