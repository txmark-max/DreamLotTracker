from datetime import datetime
from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Property(Base):
    __tablename__ = "properties"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    parcel_number: Mapped[str | None] = mapped_column(String)
    address: Mapped[str] = mapped_column(String, nullable=False)
    city: Mapped[str] = mapped_column(String, nullable=False)
    county: Mapped[str] = mapped_column(String, default="Baldwin")
    state: Mapped[str] = mapped_column(String, default="AL")
    zip_code: Mapped[str | None] = mapped_column(String)
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)
    acres: Mapped[float] = mapped_column(Float, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    listings = relationship("Listing", back_populates="property", cascade="all, delete-orphan")
    scores = relationship("ScoreComponent", back_populates="property", uselist=False, cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="property", cascade="all, delete-orphan")


class Listing(Base):
    __tablename__ = "listings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id"))
    mls_number: Mapped[str | None] = mapped_column(String)
    source: Mapped[str | None] = mapped_column(String)
    url: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String, default="Active")
    asking_price: Mapped[float] = mapped_column(Float, default=0)
    days_on_market: Mapped[int | None] = mapped_column(Integer)

    property = relationship("Property", back_populates="listings")
    price_history = relationship("PriceHistory", back_populates="listing", cascade="all, delete-orphan")


class PriceHistory(Base):
    __tablename__ = "price_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    listing_id: Mapped[int] = mapped_column(ForeignKey("listings.id"))
    price: Mapped[float] = mapped_column(Float, default=0)
    recorded_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    note: Mapped[str | None] = mapped_column(Text)

    listing = relationship("Listing", back_populates="price_history")


class Utility(Base):
    __tablename__ = "utilities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id"))
    electric: Mapped[str | None] = mapped_column(String)
    county_water: Mapped[str | None] = mapped_column(String)
    public_sewer: Mapped[str | None] = mapped_column(String)
    septic_required: Mapped[bool | None] = mapped_column(Boolean)
    fiber: Mapped[str | None] = mapped_column(String)
    notes: Mapped[str | None] = mapped_column(Text)


class Restriction(Base):
    __tablename__ = "restrictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id"))
    hoa: Mapped[str | None] = mapped_column(String)
    hoa_fee: Mapped[float | None] = mapped_column(Float)
    shop_allowed: Mapped[bool | None] = mapped_column(Boolean)
    rv_allowed: Mapped[bool | None] = mapped_column(Boolean)
    boat_allowed: Mapped[bool | None] = mapped_column(Boolean)
    livestock_allowed: Mapped[bool | None] = mapped_column(Boolean)
    notes: Mapped[str | None] = mapped_column(Text)


class LocationMetric(Base):
    __tablename__ = "location_metrics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id"))
    miles_to_gulf_shores: Mapped[float | None] = mapped_column(Float)
    minutes_to_gulf_shores: Mapped[int | None] = mapped_column(Integer)
    flood_zone: Mapped[str | None] = mapped_column(String)
    wetlands: Mapped[str | None] = mapped_column(String)
    road_type: Mapped[str | None] = mapped_column(String)
    paved_road: Mapped[bool | None] = mapped_column(Boolean)


class Financial(Base):
    __tablename__ = "financials"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id"))
    estimated_market_value: Mapped[float | None] = mapped_column(Float)
    recommended_offer: Mapped[float | None] = mapped_column(Float)
    maximum_offer: Mapped[float | None] = mapped_column(Float)
    annual_taxes: Mapped[float | None] = mapped_column(Float)
    estimated_site_prep: Mapped[float | None] = mapped_column(Float)


class ScoreComponent(Base):
    __tablename__ = "score_components"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id"))
    price_score: Mapped[float | None] = mapped_column(Float)
    location_score: Mapped[float | None] = mapped_column(Float)
    utilities_score: Mapped[float | None] = mapped_column(Float)
    flood_score: Mapped[float | None] = mapped_column(Float)
    buildability_score: Mapped[float | None] = mapped_column(Float)
    restrictions_score: Mapped[float | None] = mapped_column(Float)
    dream_score: Mapped[float | None] = mapped_column(Float)
    negotiation_grade: Mapped[str | None] = mapped_column(String)
    recommendation: Mapped[str | None] = mapped_column(String)

    property = relationship("Property", back_populates="scores")


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id"))
    pros: Mapped[str | None] = mapped_column(Text)
    cons: Mapped[str | None] = mapped_column(Text)
    questions: Mapped[str | None] = mapped_column(Text)
    builder_notes: Mapped[str | None] = mapped_column(Text)
    final_recommendation: Mapped[str | None] = mapped_column(Text)

    property = relationship("Property", back_populates="notes")


class Setting(Base):
    __tablename__ = "settings"

    key: Mapped[str] = mapped_column(String, primary_key=True)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
