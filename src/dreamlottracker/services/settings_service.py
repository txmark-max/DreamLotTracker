from dreamlottracker.repositories.setting_repository import SettingRepository


class SettingsService:
    DEFAULTS = {
        "max_price": ("125000", "Maximum lot price"),
        "target_price_per_acre": ("90000", "Target price per acre"),
        "min_acres": ("0.5", "Minimum lot size in acres"),
        "max_acres": ("2.0", "Maximum lot size in acres"),
        "ideal_acres": ("1.25", "Ideal lot size in acres"),
        "max_distance_miles": ("45", "Maximum distance from Gulf Shores in miles"),
        "target_drive_minutes_gulf_shores": ("45", "Target drive time to Gulf Shores in minutes"),
        "preferred_cities": (
            "Robertsdale, Silverhill, Summerdale, Elberta, Loxley",
            "Preferred search cities",
        ),
        "max_hoa": ("0", "Maximum HOA amount preferred"),
        "minimum_dream_score": ("85", "Minimum Dream Score for watch list"),

        # Dream Engine weights. These should total roughly 100, but the engine normalizes them.
        "weight_price": ("28", "Dream Score weight for price/value"),
        "weight_location": ("22", "Dream Score weight for location/drive time/acreage"),
        "weight_utilities": ("15", "Dream Score weight for utility availability"),
        "weight_flood": ("12", "Dream Score weight for flood/wetlands risk"),
        "weight_restrictions": ("13", "Dream Score weight for HOA and use restrictions"),
        "weight_buildability": ("10", "Dream Score weight for buildability/site readiness"),
    }

    def __init__(self):
        self.repository = SettingRepository()
        self.repository.ensure_defaults(self.DEFAULTS)

    def get_settings(self) -> dict[str, str]:
        settings = self.repository.get_all()

        for key, (default_value, _) in self.DEFAULTS.items():
            settings.setdefault(key, default_value)

        return settings

    def save_settings(self, settings: dict[str, str]) -> None:
        for key, value in settings.items():
            description = self.DEFAULTS.get(key, ("", None))[1]
            self.repository.set(key, value, description)
