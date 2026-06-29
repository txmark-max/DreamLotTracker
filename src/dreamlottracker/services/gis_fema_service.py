import subprocess
import urllib.parse


class GISFEMAService:
    FEMA_MSC_SEARCH_URL = "https://msc.fema.gov/portal/search"
    FEMA_NFHL_VIEWER_URL = "https://www.arcgis.com/apps/webappviewer/index.html?id=8b0adb51996444d4879338b5529aa9cd"
    BALDWIN_PARCEL_VIEWER_URL = "https://isv.kcsgis.com/al.baldwin_revenue/"
    BALDWIN_PROPERTY_SEARCH_URL = "https://baldwinproperty.countygovservices.com/"

    def open_fema_map_service_center(self, property_) -> None:
        query = self._best_search_query(property_)
        url = self.FEMA_MSC_SEARCH_URL

        if query:
            # FEMA's search page is the stable entry point. Some FEMA URL parameters
            # change over time, so we open the search page and copy the query to clipboard.
            self._copy_to_clipboard(query)

        self._open_url(url)

    def open_fema_nfhl_viewer(self, property_) -> None:
        # The public ArcGIS NFHL viewer is the most reliable public visual tool.
        self._open_url(self.FEMA_NFHL_VIEWER_URL)

    def open_baldwin_parcel_viewer(self, property_) -> None:
        self._open_url(self.BALDWIN_PARCEL_VIEWER_URL)

    def open_baldwin_property_search(self, property_) -> None:
        self._open_url(self.BALDWIN_PROPERTY_SEARCH_URL)

    def fema_search_text(self, property_) -> str:
        return self._best_search_query(property_)

    def _best_search_query(self, property_) -> str:
        if property_.latitude is not None and property_.longitude is not None:
            # FEMA MSC accepts decimal coordinates in longitude, latitude order.
            return f"{property_.longitude:.6f}, {property_.latitude:.6f}"

        address_parts = [
            property_.address or "",
            property_.city or "",
            property_.state or "",
            property_.zip_code or "",
        ]
        return " ".join(part for part in address_parts if part).strip()

    def _open_url(self, url: str) -> None:
        subprocess.run(["open", url], check=False)

    def _copy_to_clipboard(self, text: str) -> None:
        subprocess.run("pbcopy", input=text.encode("utf-8"), check=False)
