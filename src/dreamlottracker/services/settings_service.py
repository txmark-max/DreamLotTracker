from dreamlottracker.repositories.setting_repository import SettingRepository


class SettingsService:
    DEFAULTS = {
        "max_price": ("125000", "Maximum lot price"),
        "min_acres": ("0.5", "Minimum lot size in acres"),
        "max_acres": ("2.0", "Maximum lot size in acres"),
        "max_distance_miles": ("45", "Maximum distance from Gulf Shores in miles"),
        "preferred_cities": (
            "Robertsdale, Silverhill, Summerdale, Elberta, Loxley",
            "Preferred search cities",
        ),
        "max_hoa": ("0", "Maximum HOA amount preferred"),
        "minimum_dream_score": ("85", "Minimum Dream Score for watch list"),
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
