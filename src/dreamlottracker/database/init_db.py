from dreamlottracker.database import Base, engine
from dreamlottracker.database.models import Property
from dreamlottracker.database.session import SessionLocal


def init_database() -> None:
    Base.metadata.create_all(bind=engine)
    seed_properties()


def seed_properties() -> None:
    with SessionLocal() as session:
        existing = session.query(Property).count()
        if existing > 0:
            return

        properties = [
            Property(address="County Rd 87", city="Robertsdale", asking_price=80000, acres=1.00, dream_score=98, recommendation="Dream Lot"),
            Property(address="Sedlack Rd", city="Silverhill", asking_price=74000, acres=0.97, dream_score=97, recommendation="Dream Lot"),
            Property(address="Ponderosa Farm Rd", city="Robertsdale", asking_price=100000, acres=1.17, dream_score=95, recommendation="Strong Buy"),
        ]

        session.add_all(properties)
        session.commit()
