from PySide6.QtWidgets import QDialog, QDialogButtonBox, QMessageBox, QScrollArea, QTabWidget, QVBoxLayout, QWidget

from dreamlottracker.services.property_service import PropertyService
from dreamlottracker.ui.property_workspace.analysis_tab import AnalysisTab
from dreamlottracker.ui.property_workspace.completion_widget import CompletionWidget
from dreamlottracker.ui.property_workspace.dashboard_header import DashboardHeader
from dreamlottracker.ui.property_workspace.documents_tab import DocumentsTab
from dreamlottracker.ui.property_workspace.financial_tab import FinancialTab
from dreamlottracker.ui.property_workspace.history_tab import HistoryTab
from dreamlottracker.ui.property_workspace.listing_tab import ListingTab
from dreamlottracker.ui.property_workspace.location_tab import LocationTab
from dreamlottracker.ui.property_workspace.notes_tab import NotesTab
from dreamlottracker.ui.property_workspace.overview_tab import OverviewTab
from dreamlottracker.ui.property_workspace.photos_tab import PhotosTab
from dreamlottracker.ui.property_workspace.restrictions_tab import RestrictionsTab
from dreamlottracker.ui.property_workspace.scores_tab import ScoresTab
from dreamlottracker.ui.property_workspace.utilities_tab import UtilitiesTab


class PropertyWorkspace(QDialog):
    def __init__(self, property_id: int, parent=None):
        super().__init__(parent)

        self.property_id = property_id
        self.service = PropertyService()
        self.property_ = self.service.get_property(property_id)

        if not self.property_:
            QMessageBox.warning(self, "Property Not Found", "Property could not be loaded.")
            self.reject()
            return

        self.setWindowTitle(f"Property Dashboard - {self.property_.address}")
        self.resize(1080, 820)

        outer_layout = QVBoxLayout()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(DashboardHeader(self.property_))
        layout.addWidget(CompletionWidget(self.property_id))

        self.overview_tab = OverviewTab(self.property_)
        self.listing_tab = ListingTab(self.property_)
        self.location_tab = LocationTab(self.property_)
        self.financial_tab = FinancialTab(self.property_)
        self.utilities_tab = UtilitiesTab(self.property_)
        self.restrictions_tab = RestrictionsTab(self.property_)
        self.scores_tab = ScoresTab(self.property_)
        self.notes_tab = NotesTab(self.property_)

        tabs = QTabWidget()
        tabs.addTab(self.overview_tab, "Overview")
        tabs.addTab(self.listing_tab, "Listing")
        tabs.addTab(self.location_tab, "Location")
        tabs.addTab(self.financial_tab, "Financial")
        tabs.addTab(self.utilities_tab, "Utilities")
        tabs.addTab(self.restrictions_tab, "Restrictions")
        tabs.addTab(self.scores_tab, "Scores")
        tabs.addTab(AnalysisTab(self.property_id), "Analysis")
        tabs.addTab(PhotosTab(self.property_), "Photos")
        tabs.addTab(DocumentsTab(self.property_), "Documents")
        tabs.addTab(HistoryTab(self.property_), "History")
        tabs.addTab(self.notes_tab, "Notes")

        layout.addWidget(tabs)
        content.setLayout(layout)
        scroll.setWidget(content)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Close)
        buttons.accepted.connect(self.save)
        buttons.rejected.connect(self.reject)

        outer_layout.addWidget(scroll)
        outer_layout.addWidget(buttons)
        self.setLayout(outer_layout)

    def save(self):
        data = {}
        data.update(self.overview_tab.values())
        data.update(self.listing_tab.values())
        data.update(self.location_tab.values())
        data.update(self.financial_tab.values())
        data.update(self.utilities_tab.values())
        data.update(self.restrictions_tab.values())
        data.update(self.scores_tab.values())
        data.update(self.notes_tab.values())

        self.service.update_property_workspace(
            property_id=self.property_id,
            **data,
        )
        self.service.recalculate_scores()

        QMessageBox.information(self, "Saved", "Property dashboard saved.")
        self.accept()
