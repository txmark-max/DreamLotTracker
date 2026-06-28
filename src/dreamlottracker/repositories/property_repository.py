from dreamlottracker.database.models import Property
from dreamlottracker.database.session import SessionLocal


class PropertyRepository:
    def get_all(self) -> list[Property]:
        with SessionLocal() as session:
            return session.query(Property).order_by(Property.dream_score.desc()).all()

    def count(self) -> int:
        with SessionLocal() as session:
            return session.query(Property).count()

    def add(self, property_: Property) -> Property:
        with SessionLocal() as session:
            session.add(property_)
            session.commit()
            session.refresh(property_)
            return property_
