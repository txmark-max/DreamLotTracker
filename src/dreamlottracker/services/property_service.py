from dreamlottracker.database.models import Listing, Property, ScoreComponent
from dreamlottracker.repositories.property_repository import PropertyRepository
from dreamlottracker.services.scoring_service import ScoringService


class PropertyService:
    def __init__(self):
        self.repository = PropertyRepository()

    def get_all_properties(self) -> list[Property]:
        return self.repository.get_all()

    def get_property(self, property_id: int) -> Property | None:
        return self.repository.get_by_id(property_id)

    def get_dashboard_stats(self) -> dict:
        return {
            "total": self.repository.count(),
            "active": self.repository.active_count(),
            "dream_lots": self.repository.dream_lot_count(),
            "average_score": self.repository.average_score(),
        }

    def recalculate_scores(self) -> int:
        return ScoringService().recalculate_all()

    def add_property(self, address: str, city: str, acres: float, asking_price: float, dream_score: float, status: str = "Active") -> Property:
        prop = Property(address=address, city=city, county="Baldwin", state="AL", acres=acres)
        prop.listings.append(Listing(source="Manual", status=status, asking_price=asking_price))
        prop.scores = ScoreComponent(dream_score=dream_score, recommendation=self._recommendation_for_score(dream_score))
        saved = self.repository.add(prop)
        self.recalculate_scores()
        return saved

    def update_property_workspace(self, **kwargs) -> None:
        self.repository.update_workspace(**kwargs)

    def update_property(self, property_id: int, address: str, city: str, acres: float, asking_price: float, dream_score: float, status: str) -> None:
        updated = Property(address=address, city=city, county="Baldwin", state="AL", acres=acres)
        updated.listings.append(Listing(source="Manual", status=status, asking_price=asking_price))
        updated.scores = ScoreComponent(dream_score=dream_score, recommendation=self._recommendation_for_score(dream_score))
        self.repository.update(property_id, updated)
        self.recalculate_scores()

    def delete_property(self, property_id: int) -> None:
        self.repository.delete(property_id)
        self.recalculate_scores()

    def _recommendation_for_score(self, score: float) -> str:
        if score >= 95:
            return "Dream Lot"
        if score >= 90:
            return "Strong Buy"
        if score >= 85:
            return "Watch List"
        return "Pass"
