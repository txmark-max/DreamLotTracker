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

    def add(self, property_: Property) -> Property:
        with SessionLocal() as session:
            session.add(property_)
            session.commit()
            session.refresh(property_)
            return property_

    def update(self, property_id: int, updated: Property) -> None:
        with SessionLocal() as session:
            prop = session.query(Property).get(property_id)
            if not prop:
                return

            prop.address = updated.address
            prop.city = updated.city
            prop.acres = updated.acres
            session.commit()

    def delete(self, property_id: int) -> None:
        with SessionLocal() as session:
            prop = session.query(Property).get(property_id)
            if prop:
                session.delete(prop)
                session.commit()
