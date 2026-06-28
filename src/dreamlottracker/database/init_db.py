from dreamlottracker.database import Base, engine
from dreamlottracker.database.models import Listing, Property, ScoreComponent
from dreamlottracker.database.session import SessionLocal


def init_database() -> None:
    Base.metadata.create_all(bind=engine)
    seed_properties()


def seed_properties() -> None:
    with SessionLocal() as session:
        existing = session.query(Property).count()
        if existing > 0:
            return

        seed_data = [
            ("County Rd 87", "Robertsdale", 1.00, 80000, 98, "Dream Lot"),
            ("Sedlack Rd", "Silverhill", 0.97, 74000, 97, "Dream Lot"),
            ("Ponderosa Farm Rd", "Robertsdale", 1.17, 100000, 95, "Strong Buy"),
        ]

        for address, city, acres, price, score, recommendation in seed_data:
            prop = Property(
                address=address,
                city=city,
                county="Baldwin",
                state="AL",
                acres=acres,
            )

            prop.listings.append(
                Listing(
                    source="Seed",
                    status="Active",
                    asking_price=price,
                )
            )

            prop.scores = ScoreComponent(
                dream_score=score,
                recommendation=recommendation,
            )

            session.add(prop)

        session.commit()
