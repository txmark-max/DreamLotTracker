from dataclasses import dataclass

from dreamlottracker.database.models import Property
from dreamlottracker.services.property_service import PropertyService
from dreamlottracker.services.settings_service import SettingsService


@dataclass
class PropertyAnalysis:
    summary: str
    recommendation: str
    negotiation_strength: str
    suggested_offer: float
    maximum_offer: float
    strengths: list[str]
    concerns: list[str]
    missing_data: list[str]
    due_diligence: list[str]


class AnalysisService:
    def __init__(self):
        self.property_service = PropertyService()
        self.settings_service = SettingsService()

    def analyze_property(self, property_id: int) -> PropertyAnalysis:
        property_ = self.property_service.get_property(property_id)

        if not property_:
            return PropertyAnalysis(
                summary="Property could not be loaded.",
                recommendation="Unavailable",
                negotiation_strength="Unknown",
                suggested_offer=0,
                maximum_offer=0,
                strengths=[],
                concerns=["Property record could not be loaded."],
                missing_data=[],
                due_diligence=[],
            )

        settings = self.settings_service.get_settings()
        strengths = self._strengths(property_, settings)
        concerns = self._concerns(property_, settings)
        missing_data = self._missing_data(property_)
        due_diligence = self._due_diligence(property_, missing_data)

        listing = property_.listings[0] if property_.listings else None
        scores = property_.scores
        financials = property_.financials

        price = float(listing.asking_price) if listing else 0
        dream_score = float(scores.dream_score) if scores and scores.dream_score is not None else 0
        recommendation = scores.recommendation if scores and scores.recommendation else self._recommendation_from_score(dream_score)

        suggested_offer, maximum_offer = self._offer_range(property_)
        negotiation_strength = self._negotiation_strength(property_, suggested_offer)

        summary = self._summary(
            property_=property_,
            price=price,
            dream_score=dream_score,
            recommendation=recommendation,
            strengths=strengths,
            concerns=concerns,
            missing_data=missing_data,
        )

        return PropertyAnalysis(
            summary=summary,
            recommendation=recommendation,
            negotiation_strength=negotiation_strength,
            suggested_offer=suggested_offer,
            maximum_offer=maximum_offer,
            strengths=strengths,
            concerns=concerns,
            missing_data=missing_data,
            due_diligence=due_diligence,
        )

    def _strengths(self, property_: Property, settings: dict[str, str]) -> list[str]:
        strengths = []

        listing = property_.listings[0] if property_.listings else None
        utilities = property_.utilities
        restrictions = property_.restrictions
        location = property_.location_metrics
        scores = property_.scores

        price = float(listing.asking_price) if listing else 0
        acres = float(property_.acres or 0)
        max_price = self._float(settings.get("max_price"), 125000)
        ideal_acres = self._float(settings.get("ideal_acres"), 1.25)
        preferred_cities = {
            city.strip().lower()
            for city in settings.get("preferred_cities", "").split(",")
            if city.strip()
        }

        if price and price <= max_price:
            strengths.append(f"Asking price is within your ${max_price:,.0f} target.")

        if acres:
            if abs(acres - ideal_acres) <= 0.35:
                strengths.append(f"Lot size of {acres:.2f} acres is close to your ideal acreage.")
            elif 0.5 <= acres <= 2.0:
                strengths.append(f"Lot size of {acres:.2f} acres is within your preferred range.")

        if preferred_cities and (property_.city or "").strip().lower() in preferred_cities:
            strengths.append(f"{property_.city} is one of your preferred cities.")

        if utilities:
            if utilities.electric in ("At Road", "Available"):
                strengths.append("Electric service appears available or nearby.")
            if utilities.county_water == "Available":
                strengths.append("County water appears available.")
            if utilities.fiber == "Available":
                strengths.append("Fiber internet appears available.")

        if restrictions:
            if restrictions.hoa in ("None", "No"):
                strengths.append("No HOA is indicated.")
            if restrictions.shop_allowed:
                strengths.append("Shop/outbuilding appears allowed.")
            if restrictions.rv_allowed:
                strengths.append("RV storage/use appears allowed.")
            if restrictions.boat_allowed:
                strengths.append("Boat storage appears allowed.")

        if location:
            if location.flood_zone == "X":
                strengths.append("Flood zone is marked X, which is favorable.")
            if location.wetlands == "None":
                strengths.append("No wetlands are currently indicated.")
            if location.paved_road:
                strengths.append("Property appears to have paved-road access.")
            if location.minutes_to_gulf_shores and location.minutes_to_gulf_shores <= 45:
                strengths.append(f"Drive time to Gulf Shores is within target at {location.minutes_to_gulf_shores} minutes.")

        if scores and scores.price_score and scores.price_score >= 90:
            strengths.append("Price/value score is strong.")

        return strengths or ["No major strengths have been identified yet because more data is needed."]

    def _concerns(self, property_: Property, settings: dict[str, str]) -> list[str]:
        concerns = []

        listing = property_.listings[0] if property_.listings else None
        utilities = property_.utilities
        restrictions = property_.restrictions
        location = property_.location_metrics

        price = float(listing.asking_price) if listing else 0
        acres = float(property_.acres or 0)
        max_price = self._float(settings.get("max_price"), 125000)
        max_acres = self._float(settings.get("max_acres"), 2.0)
        min_acres = self._float(settings.get("min_acres"), 0.5)
        target_minutes = self._float(settings.get("target_drive_minutes_gulf_shores"), 45)

        if price and price > max_price:
            concerns.append(f"Asking price is above your ${max_price:,.0f} target.")

        if acres and acres < min_acres:
            concerns.append(f"Lot size is below your {min_acres:.2f}-acre minimum.")
        elif acres and acres > max_acres:
            concerns.append(f"Lot size is above your {max_acres:.2f}-acre maximum preference.")

        if utilities:
            if utilities.electric in ("Unavailable", "Unknown", None):
                concerns.append("Electric availability is not confirmed.")
            if utilities.county_water in ("Unavailable", "Unknown", None):
                concerns.append("County water availability is not confirmed.")
            if utilities.public_sewer == "Unavailable" and not utilities.septic_required:
                concerns.append("Sewer is unavailable and septic need is not clearly confirmed.")
        else:
            concerns.append("Utility details are not entered yet.")

        if restrictions:
            if restrictions.hoa == "Yes":
                concerns.append("HOA is indicated.")
            if restrictions.hoa_fee and restrictions.hoa_fee > 0:
                concerns.append(f"HOA fee is listed as ${restrictions.hoa_fee:,.0f}.")
            if restrictions.mobile_home_allowed:
                concerns.append("Mobile homes allowed may affect surrounding property standards.")
        else:
            concerns.append("Restrictions have not been verified.")

        if location:
            if location.flood_zone == "AE":
                concerns.append("Flood zone AE may add insurance/building requirements.")
            elif location.flood_zone == "VE":
                concerns.append("Flood zone VE is a major coastal flood-risk concern.")
            elif location.flood_zone == "Unknown":
                concerns.append("Flood zone is unknown.")

            if location.wetlands == "Confirmed":
                concerns.append("Wetlands are confirmed and may limit buildability.")
            elif location.wetlands == "Possible":
                concerns.append("Possible wetlands need verification.")

            if location.minutes_to_gulf_shores and location.minutes_to_gulf_shores > target_minutes:
                concerns.append(f"Drive time to Gulf Shores is above target at {location.minutes_to_gulf_shores} minutes.")
        else:
            concerns.append("Location risk details are not entered yet.")

        return concerns or ["No major concerns identified from currently entered data."]

    def _missing_data(self, property_: Property) -> list[str]:
        missing = []

        listing = property_.listings[0] if property_.listings else None
        utilities = property_.utilities
        restrictions = property_.restrictions
        location = property_.location_metrics
        financials = property_.financials

        if not property_.parcel_number:
            missing.append("Parcel number")
        if property_.latitude is None or property_.longitude is None:
            missing.append("GPS coordinates")
        if not listing or not listing.url:
            missing.append("Listing URL")
        if not listing or not listing.days_on_market:
            missing.append("Days on market")
        if not utilities:
            missing.append("Utility details")
        else:
            if not utilities.electric or utilities.electric == "Unknown":
                missing.append("Electric availability")
            if not utilities.county_water or utilities.county_water == "Unknown":
                missing.append("County water availability")
            if not utilities.fiber or utilities.fiber == "Unknown":
                missing.append("Fiber availability")
        if not restrictions:
            missing.append("Restrictions/HOA details")
        if not location:
            missing.append("Location/flood details")
        else:
            if not location.flood_zone or location.flood_zone == "Unknown":
                missing.append("Flood zone")
            if not location.wetlands or location.wetlands == "Unknown":
                missing.append("Wetlands status")
            if not location.minutes_to_gulf_shores:
                missing.append("Drive time to Gulf Shores")
        if not financials:
            missing.append("Financial estimates")
        else:
            if not financials.annual_taxes:
                missing.append("Annual taxes")
            if not financials.estimated_site_prep:
                missing.append("Site prep estimate")

        return missing

    def _due_diligence(self, property_: Property, missing_data: list[str]) -> list[str]:
        tasks = []

        if "Parcel number" in missing_data:
            tasks.append("Pull the county parcel record and enter the parcel number.")
        if "GPS coordinates" in missing_data:
            tasks.append("Confirm GPS coordinates from the listing, GIS map, or Google Maps.")
        if "Flood zone" in missing_data:
            tasks.append("Check the FEMA flood map or county GIS flood layer.")
        if "Wetlands status" in missing_data:
            tasks.append("Check wetlands layers and consider a wetlands professional if needed.")
        if "Utility details" in missing_data or "Electric availability" in missing_data:
            tasks.append("Call the power provider to confirm electric availability and connection cost.")
        if "County water availability" in missing_data:
            tasks.append("Confirm county water availability and tap fees.")
        if "Restrictions/HOA details" in missing_data:
            tasks.append("Ask for recorded restrictions, covenants, and HOA documents.")
        if "Annual taxes" in missing_data:
            tasks.append("Pull property tax history from the county revenue/tax office.")
        if "Site prep estimate" in missing_data:
            tasks.append("Estimate clearing, driveway, septic, and utility connection costs.")
        if not property_.documents:
            tasks.append("Attach survey, GIS screenshots, FEMA map, restrictions, and listing documents.")
        if not property_.photos:
            tasks.append("Add listing photos and site-visit photos.")

        return tasks or ["No immediate due-diligence gaps identified from current data."]

    def _offer_range(self, property_: Property) -> tuple[float, float]:
        listing = property_.listings[0] if property_.listings else None
        financials = property_.financials
        scores = property_.scores

        asking_price = float(listing.asking_price) if listing else 0

        if asking_price <= 0:
            return 0, 0

        market_value = float(financials.estimated_market_value) if financials and financials.estimated_market_value else 0
        site_prep = float(financials.estimated_site_prep) if financials and financials.estimated_site_prep else 0
        score = float(scores.dream_score) if scores and scores.dream_score else 75

        if market_value > 0:
            value_anchor = min(asking_price, market_value)
        else:
            value_anchor = asking_price

        condition_adjustment = 0
        if score >= 95:
            condition_adjustment = 0.96
        elif score >= 90:
            condition_adjustment = 0.94
        elif score >= 82:
            condition_adjustment = 0.90
        else:
            condition_adjustment = 0.85

        suggested = value_anchor * condition_adjustment

        if site_prep:
            suggested -= min(site_prep * 0.20, asking_price * 0.08)

        maximum = min(asking_price, value_anchor * 0.98)

        if suggested > maximum:
            suggested = maximum * 0.95

        return round(max(suggested, 0), -2), round(maximum, -2)

    def _negotiation_strength(self, property_: Property, suggested_offer: float) -> str:
        listing = property_.listings[0] if property_.listings else None
        scores = property_.scores

        if not listing or not listing.asking_price:
            return "Unknown"

        price = float(listing.asking_price)
        score = float(scores.dream_score) if scores and scores.dream_score else 0

        discount = (price - suggested_offer) / price if price else 0

        if listing.days_on_market and listing.days_on_market >= 90:
            return "High"
        if discount >= 0.10:
            return "High"
        if score < 82:
            return "Medium"
        if discount >= 0.05:
            return "Medium"
        return "Low"

    def _summary(
        self,
        property_: Property,
        price: float,
        dream_score: float,
        recommendation: str,
        strengths: list[str],
        concerns: list[str],
        missing_data: list[str],
    ) -> str:
        address = property_.address
        city = property_.city

        if dream_score >= 90:
            opening = f"{address} in {city} is currently a strong candidate."
        elif dream_score >= 82:
            opening = f"{address} in {city} is worth watching, but it needs more verification."
        else:
            opening = f"{address} in {city} has enough concerns that it should be reviewed carefully before moving forward."

        price_text = f"The asking price is ${price:,.0f}." if price else "The asking price is not entered."

        strength_text = strengths[0] if strengths else "No standout strength is currently identified."
        concern_text = concerns[0] if concerns else "No major concern is currently identified."

        missing_text = ""
        if missing_data:
            missing_text = f" There are {len(missing_data)} missing data items that should be verified before making a decision."

        return (
            f"{opening} {price_text} Current recommendation is {recommendation} "
            f"with a Dream Score of {dream_score:.1f}. Key strength: {strength_text} "
            f"Key concern: {concern_text}.{missing_text}"
        )

    def _recommendation_from_score(self, score: float) -> str:
        if score >= 95:
            return "Dream Lot"
        if score >= 90:
            return "Strong Buy"
        if score >= 82:
            return "Watch List"
        return "Pass"

    def _float(self, value, default: float) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return default
