from PySide6.QtWidgets import (
    QListWidget,
    QListWidgetItem,
    QHBoxLayout,
    QMainWindow,
    QStackedWidget,
    QStatusBar,
    QWidget,
)

from dreamlottracker.ui.compare_page import ComparePage
from dreamlottracker.ui.dashboard_page import DashboardPage
from dreamlottracker.ui.import_page import ImportPage
from dreamlottracker.ui.maps_page import MapsPage
from dreamlottracker.ui.placeholder_page import PlaceholderPage
from dreamlottracker.ui.properties_page import PropertiesPage
from dreamlottracker.ui.reports_page import ReportsPage
from dreamlottracker.ui.settings_page import SettingsPage
from dreamlottracker.version import APP_NAME


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_NAME)
        self.resize(1200, 750)

        self.navigation = QListWidget()
        self.navigation.setFixedWidth(180)

        self.pages = QStackedWidget()

        self._add_page("Dashboard", DashboardPage())
        self._add_page("Properties", PropertiesPage())
        self._add_page("Import", ImportPage())
        self._add_page("Compare", ComparePage())
        self._add_page("Financial", PlaceholderPage("Financial"))
        self._add_page("Reports", ReportsPage())
        self._add_page("Maps", MapsPage())
        self._add_page("Settings", SettingsPage())

        self.navigation.currentRowChanged.connect(self.pages.setCurrentIndex)
        self.navigation.setCurrentRow(0)

        root = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.navigation)
        layout.addWidget(self.pages)

        root.setLayout(layout)
        self.setCentralWidget(root)

        status = QStatusBar()
        status.showMessage("Database Connected ✓    Ready")
        self.setStatusBar(status)

    def _add_page(self, name: str, widget: QWidget):
        self.navigation.addItem(QListWidgetItem(name))
        self.pages.addWidget(widget)
