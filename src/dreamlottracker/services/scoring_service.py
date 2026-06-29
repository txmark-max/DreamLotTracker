from dreamlottracker.database.models import Property, ScoreComponent
from dreamlottracker.repositories.property_repository import PropertyRepository
from dreamlottracker.services.settings_service import SettingsService


class ScoringService:
    def __init__(self):
        self.property_repository = PropertyRepository()
        self.settings_service = SettingsService()

    def recalculate_all(self) -> int:
        properties = self.property_repository.get_all()
        for property_ in properties:
            scores = self.calculate_scores(property_)
            self.property_repository.update_scores(property_.id, scores)
        return len(properties)

    def calculate_scores(self, property_: Property) -> ScoreComponent:
        settings = self.settings_service.get_settings()
        max_price = float(settings.get("max_price", 125000))
        min_acres = float(settings.get("min_acres", 0.5))
        max_acres = float(settings.get("max_acres", 2.0))

        listing = property_.listings[0] if property_.listings else None
        price = listing.asking_price if listing else 0
        status = listing.status if listing else "Unknown"

        price_score = self._price_score(price, max_price)
        acreage_score = self._acreage_score(property_.acres, min_acres, max_acres)
        status_score = 100 if status == "Active" else 70 if status == "Watch" else 50
        utilities_score = self._utilities_score(property_)
        restrictions_score = self._restrictions_score(property_)
        flood_score = 80
        buildability_score = 80

        dream_score = (
            price_score * 0.30
            + acreage_score * 0.20
            + status_score * 0.10
            + utilities_score * 0.15
            + flood_score * 0.10
            + buildability_score * 0.05
            + restrictions_score * 0.10
        )

        return ScoreComponent(
            price_score=price_score,
            location_score=acreage_score,
            utilities_score=utilities_score,
            flood_score=flood_score,
            buildability_score=buildability_score,
            restrictions_score=restrictions_score,
            dream_score=round(dream_score, 1),
            negotiation_grade=self._negotiation_grade(price_score, status),
            recommendation=self._recommendation_for_score(dream_score),
        )

    def _price_score(self, price: float, max_price: float) -> float:
        if price <= 0:
            return 0
        if price <= max_price * 0.80:
            return 100
        if price <= max_price:
            return 90
        if price <= max_price * 1.10:
            return 75
        if price <= max_price * 1.25:
            return 60
        return 40

    def _acreage_score(self, acres: float, min_acres: float, max_acres: float) -> float:
        if acres < min_acres:
            return 50
        if min_acres <= acres <= max_acres:
            return 100
        if acres <= max_acres * 1.25:
            return 80
        return 60

    def _utilities_score(self, property_: Property) -> float:
        utilities = property_.utilities
        if not utilities:
            return 70
        score = 50
        if utilities.electric in ("At Road", "Available"):
            score += 15
        if utilities.county_water == "Available":
            score += 15
        if utilities.fiber in ("Available", "Planned"):
            score += 10
        if utilities.public_sewer == "Available" or utilities.septic_required is not None:
            score += 10
        return min(score, 100)

    def _restrictions_score(self, property_: Property) -> float:
        restrictions = property_.restrictions
        if not restrictions:
            return 75
        score = 70
        if restrictions.hoa in ("None", "No"):
            score += 15
        if restrictions.shop_allowed:
            score += 5
        if restrictions.rv_allowed:
            score += 5
        if restrictions.boat_allowed:
            score += 5
        if restrictions.mobile_home_allowed:
            score -= 10
        return max(min(score, 100), 0)

    def _recommendation_for_score(self, score: float) -> str:
        if score >= 95:
            return "Dream Lot"
        if score >= 90:
            return "Strong Buy"
        if score >= 85:
            return "Watch List"
        return "Pass"

    def _negotiation_grade(self, price_score: float, status: str) -> str:
        if status != "Active":
            return "B"
        if price_score >= 95:
            return "A+"
        if price_score >= 85:
            return "A"
        if price_score >= 70:
            return "B"
        return "C"
