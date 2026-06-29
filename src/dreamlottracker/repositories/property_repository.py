from sqlalchemy.orm import joinedload

from dreamlottracker.database.models import Listing, Note, PriceHistory, Property, ScoreComponent
from dreamlottracker.database.session import SessionLocal


class PropertyRepository:
    def get_all(self) -> list[Property]:
        with SessionLocal() as session:
            return (
                session.query(Property)
                .options(joinedload(Property.listings), joinedload(Property.scores))
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
            if not scores:
                return 0.0
            return sum(score[0] for score in scores) / len(scores)

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

    def update_workspace(
        self,
        property_id: int,
        address: str,
        city: str,
        county: str,
        state: str,
        zip_code: str,
        parcel_number: str,
        acres: float,
        latitude: float,
        longitude: float,
        asking_price: float,
        status: str,
        dream_score: float,
        recommendation: str,
        pros: str,
        cons: str,
        questions: str,
        builder_notes: str,
        final_recommendation: str,
    ) -> None:
        with SessionLocal() as session:
            prop = session.query(Property).options(joinedload(Property.listings), joinedload(Property.scores), joinedload(Property.notes)).get(property_id)
            if not prop:
                return

            prop.address = address
            prop.city = city
            prop.county = county
            prop.state = state
            prop.zip_code = zip_code
            prop.parcel_number = parcel_number
            prop.acres = acres
            prop.latitude = latitude if latitude != 0 else None
            prop.longitude = longitude if longitude != 0 else None

            if prop.listings:
                listing = prop.listings[0]
            else:
                listing = Listing(source="Manual")
                prop.listings.append(listing)
                session.flush()

            old_price = listing.asking_price or 0
            listing.asking_price = asking_price
            listing.status = status
            if old_price != asking_price:
                session.add(PriceHistory(listing_id=listing.id, price=asking_price, note=f"Price changed from ${old_price:,.0f}"))

            if not prop.scores:
                prop.scores = ScoreComponent()
            prop.scores.dream_score = dream_score
            prop.scores.recommendation = recommendation

            note = prop.notes[0] if prop.notes else None
            if not note:
                note = Note()
                prop.notes.append(note)
            note.pros = pros
            note.cons = cons
            note.questions = questions
            note.builder_notes = builder_notes
            note.final_recommendation = final_recommendation

            session.commit()

    def delete(self, property_id: int) -> None:
        with SessionLocal() as session:
            prop = session.query(Property).get(property_id)
            if prop:
                session.delete(prop)
                session.commit()
