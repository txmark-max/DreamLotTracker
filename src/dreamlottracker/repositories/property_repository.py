from sqlalchemy.orm import joinedload

from dreamlottracker.database.models import Listing, Property, ScoreComponent
from dreamlottracker.database.session import SessionLocal


class PropertyRepository:
    def get_all(self) -> list[Property]:
        with SessionLocal() as session:
            return (
                session.query(Property)
                .options(
                    joinedload(Property.listings),
                    joinedload(Property.scores),
                )
                .outerjoin(ScoreComponent)
                .order_by(ScoreComponent.dream_score.desc())
                .all()
            )

    def count(self) -> int:
        with SessionLocal() as session:
            return session.query(Property).count()

    def active_count(self) -> int:
        with SessionLocal() as session:
            return (
                session.query(Property)
                .join(Listing)
                .filter(Listing.status == "Active")
                .count()
            )

    def dream_lot_count(self) -> int:
        with SessionLocal() as session:
            return (
                session.query(Property)
                .join(ScoreComponent)
                .filter(ScoreComponent.dream_score >= 95)
                .count()
            )

    def average_score(self) -> float:
        with SessionLocal() as session:
            scores = (
                session.query(ScoreComponent.dream_score)
                .filter(ScoreComponent.dream_score.isnot(None))
                .all()
            )

            if not scores:
                return 0.0

            return sum(score[0] for score in scores) / len(scores)

    def add(self, property_: Property) -> Property:
        with SessionLocal() as session:
            session.add(property_)
            session.commit()
            session.refresh(property_)
            return property_

    def update(self, property_id: int, updated: Property) -> None:
        with SessionLocal() as session:
            prop = (
                session.query(Property)
                .options(
                    joinedload(Property.listings),
                    joinedload(Property.scores),
                )
                .get(property_id)
            )

            if not prop:
                return

            prop.address = updated.address
            prop.city = updated.city
            prop.acres = updated.acres

            updated_listing = updated.listings[0] if updated.listings else None

            if updated_listing:
                if prop.listings:
                    prop.listings[0].asking_price = updated_listing.asking_price
                    prop.listings[0].status = updated_listing.status
                else:
                    prop.listings.append(updated_listing)

            if updated.scores:
                if prop.scores:
                    prop.scores.dream_score = updated.scores.dream_score
                    prop.scores.recommendation = updated.scores.recommendation
                    prop.scores.price_score = updated.scores.price_score
                    prop.scores.location_score = updated.scores.location_score
                    prop.scores.utilities_score = updated.scores.utilities_score
                    prop.scores.flood_score = updated.scores.flood_score
                    prop.scores.buildability_score = updated.scores.buildability_score
                    prop.scores.restrictions_score = updated.scores.restrictions_score
                else:
                    prop.scores = updated.scores

            session.commit()

    def update_scores(self, property_id: int, scores: ScoreComponent) -> None:
        with SessionLocal() as session:
            prop = (
                session.query(Property)
                .options(joinedload(Property.scores))
                .get(property_id)
            )

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

    def delete(self, property_id: int) -> None:
        with SessionLocal() as session:
            prop = session.query(Property).get(property_id)

            if prop:
                session.delete(prop)
                session.commit()
