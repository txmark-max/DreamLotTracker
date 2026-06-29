from pathlib import Path

import pandas as pd

from dreamlottracker.database.models import Listing, Property, ScoreComponent
from dreamlottracker.repositories.property_repository import PropertyRepository


class ImportService:
    def __init__(self):
        self.property_repository = PropertyRepository()

    def load_file(self, file_path: Path) -> list[dict]:
        file_path = Path(file_path)

        if file_path.suffix.lower() == ".csv":
            dataframe = pd.read_csv(file_path)
        elif file_path.suffix.lower() in (".xlsx", ".xls"):
            dataframe = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file type. Please use CSV or Excel.")

        dataframe = dataframe.fillna("")
        normalized_rows = []

        for _, row in dataframe.iterrows():
            normalized_rows.append(self._normalize_row(row.to_dict()))

        return normalized_rows

    def import_rows(self, rows: list[dict]) -> dict:
        existing_keys = self._existing_property_keys()

        imported = 0
        skipped = 0

        for row in rows:
            address = row.get("address", "").strip()
            city = row.get("city", "").strip()

            if not address or not city:
                skipped += 1
                continue

            key = self._key(address, city)

            if key in existing_keys:
                skipped += 1
                continue

            prop = Property(
                address=address,
                city=city,
                county=row.get("county", "Baldwin") or "Baldwin",
                state=row.get("state", "AL") or "AL",
                acres=self._float(row.get("acres", 0)),
                latitude=self._optional_float(row.get("latitude", "")),
                longitude=self._optional_float(row.get("longitude", "")),
            )

            prop.listings.append(
                Listing(
                    source="Import",
                    status=row.get("status", "Active") or "Active",
                    asking_price=self._float(row.get("price", 0)),
                )
            )

            prop.scores = ScoreComponent(
                dream_score=0,
                recommendation="Imported",
            )

            self.property_repository.add(prop)
            existing_keys.add(key)
            imported += 1

        return {
            "imported": imported,
            "skipped": skipped,
            "total": len(rows),
        }

    def _existing_property_keys(self) -> set[str]:
        return {
            self._key(property_.address, property_.city)
            for property_ in self.property_repository.get_all()
        }

    def _key(self, address: str, city: str) -> str:
        return f"{address.strip().lower()}|{city.strip().lower()}"

    def _normalize_row(self, row: dict) -> dict:
        lookup = {}

        for key, value in row.items():
            normalized_key = self._normalize_header(str(key))
            lookup[normalized_key] = value

        return {
            "address": self._first(lookup, ["address", "property_address", "street_address", "location"]),
            "city": self._first(lookup, ["city", "town"]),
            "county": self._first(lookup, ["county"]),
            "state": self._first(lookup, ["state"]),
            "acres": self._first(lookup, ["acres", "acreage", "lot_size", "lot_acres"]),
            "price": self._first(lookup, ["price", "asking_price", "list_price", "listing_price"]),
            "status": self._first(lookup, ["status", "listing_status"]),
            "latitude": self._first(lookup, ["latitude", "lat"]),
            "longitude": self._first(lookup, ["longitude", "lon", "lng"]),
        }

    def _normalize_header(self, value: str) -> str:
        return (
            value.strip()
            .lower()
            .replace(" ", "_")
            .replace("-", "_")
            .replace("/", "_")
        )

    def _first(self, row: dict, keys: list[str]):
        for key in keys:
            if key in row:
                return row[key]
        return ""

    def _float(self, value) -> float:
        if value is None:
            return 0.0

        text = str(value).strip().replace("$", "").replace(",", "")

        if text == "":
            return 0.0

        try:
            return float(text)
        except ValueError:
            return 0.0

    def _optional_float(self, value):
        number = self._float(value)
        return number if number != 0 else None
