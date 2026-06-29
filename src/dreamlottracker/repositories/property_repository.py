from sqlalchemy.orm import joinedload

from dreamlottracker.database.models import (
    Financial,
    Listing,
    LocationMetric,
    Note,
    PriceHistory,
    Property,
    Restriction,
    ScoreComponent,
    Utility,
)
from dreamlottracker.database.session import SessionLocal


class PropertyRepository:
    def get_all(self) -> list[Property]:
        with SessionLocal() as session:
            return (
                session.query(Property)
                .options(
                    joinedload(Property.listings),
                    joinedload(Property.scores),
                    joinedload(Property.utilities),
                    joinedload(Property.restrictions),
                    joinedload(Property.location_metrics),
                    joinedload(Property.financials),
                )
                .outerjoin(ScoreComponent)
                .order_by(ScoreComponent.dream_score.desc())
                .all()
            )

    def get_by_id(self, property_id: int) -> Property | None:
        with SessionLocal() as session:
            return (
                session.query(Property)
                .options(
                    joinedload(Property.listings).joinedload(Listing.price_history),
                    joinedload(Property.scores),
                    joinedload(Property.notes),
                    joinedload(Property.utilities),
                    joinedload(Property.restrictions),
                    joinedload(Property.location_metrics),
                    joinedload(Property.financials),
                )
                .get(property_id)
            )

    def count(self) -> int:
        with SessionLocal() as session:
            return session.query(Property).count()

    def active_count(self) -> int:
        with SessionLocal() as session:
            return session.query(Property).join(Listing).filter(Listing.status == "Active").count()

    def dream_lot_count(self) -> int:
        with SessionLocal() as session:
            return session.query(Property).join(ScoreComponent).filter(ScoreComponent.dream_score >= 95).count()

    def average_score(self) -> float:
        with SessionLocal() as session:
            scores = session.query(ScoreComponent.dream_score).filter(ScoreComponent.dream_score.isnot(None)).all()
            return 0.0 if not scores else sum(score[0] for score in scores) / len(scores)

    def add(self, property_: Property) -> Property:
        with SessionLocal() as session:
            session.add(property_)
            session.commit()
            session.refresh(property_)
            if property_.listings:
                listing = property_.listings[0]
                session.add(PriceHistory(listing_id=listing.id, price=listing.asking_price or 0, note="Initial price"))
                session.commit()
            return property_

    def update(self, property_id: int, updated: Property) -> None:
        with SessionLocal() as session:
            prop = session.query(Property).options(joinedload(Property.listings), joinedload(Property.scores)).get(property_id)
            if not prop:
                return
            prop.address = updated.address
            prop.city = updated.city
            prop.acres = updated.acres
            updated_listing = updated.listings[0] if updated.listings else None
            if updated_listing:
                if prop.listings:
                    listing = prop.listings[0]
                    old_price = listing.asking_price or 0
                    listing.asking_price = updated_listing.asking_price
                    listing.status = updated_listing.status
                    if old_price != updated_listing.asking_price:
                        session.add(PriceHistory(listing_id=listing.id, price=updated_listing.asking_price, note=f"Price changed from ${old_price:,.0f}"))
                else:
                    prop.listings.append(updated_listing)
            if updated.scores:
                if prop.scores:
                    prop.scores.dream_score = updated.scores.dream_score
                    prop.scores.recommendation = updated.scores.recommendation
                else:
                    prop.scores = updated.scores
            session.commit()

    def update_scores(self, property_id: int, scores: ScoreComponent) -> None:
        with SessionLocal() as session:
            prop = session.query(Property).options(joinedload(Property.scores)).get(property_id)
            if not prop:
                return
            if not prop.scores:
                prop.scores = ScoreComponent()
            prop.scores.price_score = scores.price_score
            prop.scores.location_score = scores.location_score
            prop.scores.utilities_score = scores.utilities_score
            prop.scores.flood_score = scores.flood_score
            prop.scores.buildability_score = scores.buildability_score
            prop.scores.restrictions_score = scores.restrictions_score
            prop.scores.dream_score = scores.dream_score
            prop.scores.negotiation_grade = scores.negotiation_grade
            prop.scores.recommendation = scores.recommendation
            session.commit()

    def update_workspace(self, **data) -> None:
        with SessionLocal() as session:
            prop = (
                session.query(Property)
                .options(
                    joinedload(Property.listings),
                    joinedload(Property.scores),
                    joinedload(Property.notes),
                    joinedload(Property.utilities),
                    joinedload(Property.restrictions),
                    joinedload(Property.location_metrics),
                    joinedload(Property.financials),
                )
                .get(data["property_id"])
            )
            if not prop:
                return

            prop.address = data["address"]
            prop.city = data["city"]
            prop.county = data["county"]
            prop.state = data["state"]
            prop.zip_code = data["zip_code"]
            prop.parcel_number = data["parcel_number"]
            prop.acres = data["acres"]
            prop.latitude = data["latitude"] if data["latitude"] != 0 else None
            prop.longitude = data["longitude"] if data["longitude"] != 0 else None

            listing = prop.listings[0] if prop.listings else Listing(source="Manual")
            if not prop.listings:
                prop.listings.append(listing)
                session.flush()
            old_price = listing.asking_price or 0
            listing.asking_price = data["asking_price"]
            listing.status = data["status"]
            if old_price != data["asking_price"]:
                session.add(PriceHistory(listing_id=listing.id, price=data["asking_price"], note=f"Price changed from ${old_price:,.0f}"))

            if not prop.scores:
                prop.scores = ScoreComponent()
            prop.scores.dream_score = data["dream_score"]
            prop.scores.recommendation = data["recommendation"]

            note = prop.notes[0] if prop.notes else Note()
            if not prop.notes:
                prop.notes.append(note)
            note.pros = data["pros"]
            note.cons = data["cons"]
            note.questions = data["questions"]
            note.builder_notes = data["builder_notes"]
            note.final_recommendation = data["final_recommendation"]

            if not prop.utilities:
                prop.utilities = Utility()
            prop.utilities.electric = data["electric"]
            prop.utilities.county_water = data["county_water"]
            prop.utilities.public_sewer = data["public_sewer"]
            prop.utilities.septic_required = data["septic_required"]
            prop.utilities.fiber = data["fiber"]
            prop.utilities.natural_gas = data["natural_gas"]
            prop.utilities.notes = data["utility_notes"]

            if not prop.restrictions:
                prop.restrictions = Restriction()
            prop.restrictions.hoa = data["hoa"]
            prop.restrictions.hoa_fee = data["hoa_fee"]
            prop.restrictions.shop_allowed = data["shop_allowed"]
            prop.restrictions.rv_allowed = data["rv_allowed"]
            prop.restrictions.boat_allowed = data["boat_allowed"]
            prop.restrictions.livestock_allowed = data["livestock_allowed"]
            prop.restrictions.mobile_home_allowed = data["mobile_home_allowed"]
            prop.restrictions.barndominium_allowed = data["barndominium_allowed"]
            prop.restrictions.notes = data["restriction_notes"]

            if not prop.location_metrics:
                prop.location_metrics = LocationMetric()
            prop.location_metrics.miles_to_gulf_shores = data["miles_to_gulf_shores"]
            prop.location_metrics.minutes_to_gulf_shores = data["minutes_to_gulf_shores"]
            prop.location_metrics.minutes_to_foley = data["minutes_to_foley"]
            prop.location_metrics.minutes_to_fairhope = data["minutes_to_fairhope"]
            prop.location_metrics.minutes_to_pensacola = data["minutes_to_pensacola"]
            prop.location_metrics.flood_zone = data["flood_zone"]
            prop.location_metrics.wetlands = data["wetlands"]
            prop.location_metrics.road_type = data["road_type"]
            prop.location_metrics.paved_road = data["paved_road"]

            if not prop.financials:
                prop.financials = Financial()
            prop.financials.estimated_market_value = data["estimated_market_value"]
            prop.financials.recommended_offer = data["recommended_offer"]
            prop.financials.maximum_offer = data["maximum_offer"]
            prop.financials.annual_taxes = data["annual_taxes"]
            prop.financials.estimated_site_prep = data["estimated_site_prep"]
            prop.financials.estimated_clearing = data["estimated_clearing"]
            prop.financials.estimated_driveway = data["estimated_driveway"]
            prop.financials.estimated_septic = data["estimated_septic"]
            prop.financials.estimated_utilities = data["estimated_utilities"]

            session.commit()

    def delete(self, property_id: int) -> None:
        with SessionLocal() as session:
            prop = session.query(Property).get(property_id)
            if prop:
                session.delete(prop)
                session.commit()
