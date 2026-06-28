from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Property(Base):
    __tablename__ = "properties"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(String, nullable=False)
    city: Mapped[str] = mapped_column(String, nullable=False)
    county: Mapped[str] = mapped_column(String, default="Baldwin")
    state: Mapped[str] = mapped_column(String, default="AL")

    asking_price: Mapped[float] = mapped_column(Float, default=0)
    acres: Mapped[float] = mapped_column(Float, default=0)
    status: Mapped[str] = mapped_column(String, default="Active")
    recommendation: Mapped[str] = mapped_column(String, default="Watch List")
    dream_score: Mapped[float] = mapped_column(Float, default=0)
