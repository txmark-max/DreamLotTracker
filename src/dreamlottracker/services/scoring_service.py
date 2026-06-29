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

        weights = self._weights(settings)

        price_score = self._price_score(property_, settings)
        location_score = self._location_score(property_, settings)
        utilities_score = self._utilities_score(property_)
        flood_score = self._flood_score(property_)
        restrictions_score = self._restrictions_score(property_, settings)
        buildability_score = self._buildability_score(property_)

        total_weight = sum(weights.values()) or 1

        dream_score = (
            price_score * weights["price"]
            + location_score * weights["location"]
            + utilities_score * weights["utilities"]
            + flood_score * weights["flood"]
            + restrictions_score * weights["restrictions"]
            + buildability_score * weights["buildability"]
        ) / total_weight

        dream_score = round(dream_score, 1)

        return ScoreComponent(
            price_score=round(price_score, 1),
            location_score=round(location_score, 1),
            utilities_score=round(utilities_score, 1),
            flood_score=round(flood_score, 1),
            buildability_score=round(buildability_score, 1),
            restrictions_score=round(restrictions_score, 1),
            dream_score=dream_score,
            negotiation_grade=self._negotiation_grade(price_score, property_),
            recommendation=self._recommendation_for_score(dream_score),
        )

    def _weights(self, settings: dict[str, str]) -> dict[str, float]:
        return {
            "price": self._float(settings.get("weight_price"), 28),
            "location": self._float(settings.get("weight_location"), 22),
            "utilities": self._float(settings.get("weight_utilities"), 15),
            "flood": self._float(settings.get("weight_flood"), 12),
            "restrictions": self._float(settings.get("weight_restrictions"), 13),
            "buildability": self._float(settings.get("weight_buildability"), 10),
        }

    def _price_score(self, property_: Property, settings: dict[str, str]) -> float:
        listing = property_.listings[0] if property_.listings else None
        price = float(listing.asking_price) if listing else 0
        acres = float(property_.acres or 0)

        if price <= 0 or acres <= 0:
            return 0

        max_price = self._float(settings.get("max_price"), 125000)
        target_price_per_acre = self._float(settings.get("target_price_per_acre"), 90000)
        price_per_acre = price / acres

        # Overall price fit.
        if price <= max_price:
            total_price_score = 100 - max(0, (price / max_price) - 0.65) * 35
        else:
            overage_percent = (price - max_price) / max_price
            total_price_score = 85 - overage_percent * 120

        # Value per acre fit.
        if price_per_acre <= target_price_per_acre:
            ppa_score = 100 - max(0, (price_per_acre / target_price_per_acre) - 0.60) * 25
        else:
            overage_percent = (price_per_acre - target_price_per_acre) / target_price_per_acre
            ppa_score = 85 - overage_percent * 100

        # Blend price and price per acre to reduce tied scores.
        score = (total_price_score * 0.55) + (ppa_score * 0.45)
        return self._clamp(score)

    def _location_score(self, property_: Property, settings: dict[str, str]) -> float:
        min_acres = self._float(settings.get("min_acres"), 0.5)
        max_acres = self._float(settings.get("max_acres"), 2.0)
        ideal_acres = self._float(settings.get("ideal_acres"), 1.25)
        target_minutes = self._float(settings.get("target_drive_minutes_gulf_shores"), 45)

        acreage_score = self._acreage_score(float(property_.acres or 0), min_acres, max_acres, ideal_acres)
        drive_score = self._drive_time_score(property_, target_minutes)
        city_score = self._preferred_city_score(property_, settings)

        return self._clamp((acreage_score * 0.40) + (drive_score * 0.45) + (city_score * 0.15))

    def _acreage_score(self, acres: float, min_acres: float, max_acres: float, ideal_acres: float) -> float:
        if acres <= 0:
            return 0

        if acres < min_acres:
            return self._clamp(60 * (acres / min_acres))

        if acres > max_acres:
            over = (acres - max_acres) / max_acres
            return self._clamp(90 - over * 60)

        # Inside range. Best score close to ideal acreage.
        spread = max(max_acres - min_acres, 0.01)
        distance_from_ideal = abs(acres - ideal_acres) / spread
        return self._clamp(100 - distance_from_ideal * 25)

    def _drive_time_score(self, property_: Property, target_minutes: float) -> float:
        location = property_.location_metrics

        if not location:
            return 75

        minutes = location.minutes_to_gulf_shores or 0

        if minutes <= 0:
            # Fall back to miles only if minutes are not entered.
            miles = location.miles_to_gulf_shores or 0
            if miles <= 0:
                return 75
            estimated_minutes = miles * 1.15
            minutes = estimated_minutes

        if minutes <= target_minutes:
            return self._clamp(100 - max(0, (minutes / target_minutes) - 0.50) * 20)

        over = (minutes - target_minutes) / target_minutes
        return self._clamp(85 - over * 90)

    def _preferred_city_score(self, property_: Property, settings: dict[str, str]) -> float:
        preferred = settings.get("preferred_cities", "")
        cities = {city.strip().lower() for city in preferred.split(",") if city.strip()}

        if not cities:
            return 80

        return 100 if (property_.city or "").strip().lower() in cities else 70

    def _utilities_score(self, property_: Property) -> float:
        utilities = property_.utilities

        if not utilities:
            return 70

        score = 45

        if utilities.electric in ("At Road", "Available"):
            score += 18
        elif utilities.electric == "Nearby":
            score += 10

        if utilities.county_water == "Available":
            score += 17
        elif utilities.county_water == "Unknown":
            score += 6

        if utilities.public_sewer == "Available":
            score += 12
        elif utilities.septic_required:
            score += 7
        elif utilities.public_sewer == "Unknown":
            score += 5

        if utilities.fiber == "Available":
            score += 10
        elif utilities.fiber == "Planned":
            score += 7
        elif utilities.fiber == "Unknown":
            score += 3

        if utilities.natural_gas == "Available":
            score += 3

        return self._clamp(score)

    def _flood_score(self, property_: Property) -> float:
        location = property_.location_metrics

        if not location:
            return 80

        flood_zone = location.flood_zone or "Unknown"
        wetlands = location.wetlands or "Unknown"

        if flood_zone == "X":
            flood = 100
        elif flood_zone == "AE":
            flood = 62
        elif flood_zone == "VE":
            flood = 35
        else:
            flood = 80

        if wetlands == "Confirmed":
            flood -= 25
        elif wetlands == "Possible":
            flood -= 12
        elif wetlands == "None":
            flood += 5

        return self._clamp(flood)

    def _restrictions_score(self, property_: Property, settings: dict[str, str]) -> float:
        restrictions = property_.restrictions

        if not restrictions:
            return 75

        max_hoa = self._float(settings.get("max_hoa"), 0)
        score = 65

        if restrictions.hoa in ("None", "No"):
            score += 20
        elif restrictions.hoa == "Unknown":
            score += 5
        elif restrictions.hoa == "Yes":
            score -= 10

        hoa_fee = float(restrictions.hoa_fee or 0)
        if hoa_fee <= max_hoa:
            score += 8
        else:
            score -= min(25, (hoa_fee - max_hoa) / 20)

        if restrictions.shop_allowed:
            score += 5
        if restrictions.rv_allowed:
            score += 4
        if restrictions.boat_allowed:
            score += 4
        if restrictions.livestock_allowed:
            score += 3
        if restrictions.barndominium_allowed:
            score += 2
        if restrictions.mobile_home_allowed:
            score -= 5

        return self._clamp(score)

    def _buildability_score(self, property_: Property) -> float:
        score = 80

        location = property_.location_metrics
        utilities = property_.utilities

        if location:
            if location.road_type in ("County", "State"):
                score += 8
            elif location.road_type == "Private":
                score -= 5

            if location.paved_road:
                score += 5

            if location.wetlands == "Confirmed":
                score -= 20
            elif location.wetlands == "Possible":
                score -= 10

        if utilities:
            if utilities.electric in ("At Road", "Available"):
                score += 4
            if utilities.county_water == "Available":
                score += 4

        return self._clamp(score)

    def _recommendation_for_score(self, score: float) -> str:
        if score >= 95:
            return "Dream Lot"
        if score >= 90:
            return "Strong Buy"
        if score >= 82:
            return "Watch List"
        return "Pass"

    def _negotiation_grade(self, price_score: float, property_: Property) -> str:
        listing = property_.listings[0] if property_.listings else None
        status = listing.status if listing else "Unknown"

        if status != "Active":
            return "B"
        if price_score >= 95:
            return "A+"
        if price_score >= 88:
            return "A"
        if price_score >= 76:
            return "B"
        return "C"

    def _float(self, value, default: float) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    def _clamp(self, value: float, minimum: float = 0, maximum: float = 100) -> float:
        return max(minimum, min(maximum, value))
