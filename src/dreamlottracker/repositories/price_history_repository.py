from datetime import datetime

from dreamlottracker.database.models import Listing, PriceHistory
from dreamlottracker.database.session import SessionLocal


class PriceHistoryRepository:
    def get_for_listing(self, listing_id: int) -> list[PriceHistory]:
        with SessionLocal() as session:
            return (
                session.query(PriceHistory)
                .filter(PriceHistory.listing_id == listing_id)
                .order_by(PriceHistory.recorded_date.desc())
                .all()
            )

    def add_entry(self, listing_id: int, price: float, note: str = "") -> None:
        with SessionLocal() as session:
            entry = PriceHistory(
                listing_id=listing_id,
                price=price,
                recorded_date=datetime.utcnow(),
                note=note,
            )

            session.add(entry)
            session.commit()

    def ensure_initial_entry(self, listing: Listing) -> None:
        with SessionLocal() as session:
            existing = (
                session.query(PriceHistory)
                .filter(PriceHistory.listing_id == listing.id)
                .count()
            )

            if existing == 0:
                session.add(
                    PriceHistory(
                        listing_id=listing.id,
                        price=listing.asking_price or 0,
                        recorded_date=datetime.utcnow(),
                        note="Initial price",
                    )
                )
                session.commit()
