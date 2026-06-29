import json
import urllib.error
import urllib.request

from dreamlottracker.services.settings_service import SettingsService


class DriveTimeService:
    MATRIX_URL = "https://api.openrouteservice.org/v2/matrix/driving-car"

    def __init__(self):
        self.settings_service = SettingsService()

    def calculate_drive_times(self, latitude: float, longitude: float) -> dict[str, int]:
        settings = self.settings_service.get_settings()
        api_key = settings.get("ors_api_key", "").strip()

        if not api_key:
            raise ValueError("OpenRouteService API key is missing. Add it in Settings.")

        if not latitude or not longitude:
            raise ValueError("Property GPS coordinates are missing.")

        destinations = self._destinations(settings)

        if not destinations:
            raise ValueError("No drive-time destinations are configured.")

        # OpenRouteService expects [longitude, latitude].
        locations = [[longitude, latitude]]
        names = []

        for name, dest_latitude, dest_longitude in destinations:
            names.append(name)
            locations.append([dest_longitude, dest_latitude])

        payload = {
            "locations": locations,
            "sources": [0],
            "destinations": list(range(1, len(locations))),
            "metrics": ["duration"],
            "units": "mi",
        }

        request = urllib.request.Request(
            self.MATRIX_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": api_key,
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            message = error.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"OpenRouteService error {error.code}: {message}") from error
        except urllib.error.URLError as error:
            raise RuntimeError(f"Could not reach OpenRouteService: {error}") from error

        durations = data.get("durations", [])

        if not durations or not durations[0]:
            raise RuntimeError("OpenRouteService did not return drive-time durations.")

        result = {}

        for name, seconds in zip(names, durations[0]):
            if seconds is None:
                result[name] = 0
            else:
                result[name] = round(seconds / 60)

        return result

    def _destinations(self, settings: dict[str, str]) -> list[tuple[str, float, float]]:
        return [
            (
                "gulf_shores",
                self._float(settings.get("destination_gulf_shores_lat"), 30.2460),
                self._float(settings.get("destination_gulf_shores_lon"), -87.7008),
            ),
            (
                "foley",
                self._float(settings.get("destination_foley_lat"), 30.4066),
                self._float(settings.get("destination_foley_lon"), -87.6836),
            ),
            (
                "fairhope",
                self._float(settings.get("destination_fairhope_lat"), 30.5229),
                self._float(settings.get("destination_fairhope_lon"), -87.9033),
            ),
            (
                "pensacola",
                self._float(settings.get("destination_pensacola_lat"), 30.4213),
                self._float(settings.get("destination_pensacola_lon"), -87.2169),
            ),
        ]

    def _float(self, value, default: float) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return default
