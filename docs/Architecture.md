# Dream Lot Tracker Architecture

## Purpose

Dream Lot Tracker is a desktop land-evaluation platform for tracking, scoring, comparing, and documenting potential land purchases.

## Architecture Layers

```text
UI Layer
  PySide6 pages and dialogs

Service Layer
  Business logic, scoring, imports, exports, analysis

Repository Layer
  Database access and persistence

Database Layer
  SQLAlchemy ORM models and SQLite

File Storage Layer
  Photos, documents, reports, imports, exports
```

## Current Main Components

### UI

- DashboardPage
- PropertiesPage
- PropertyWorkspace
- ImportPage
- ComparePage
- ReportsPage
- MapsPage
- SettingsPage

### Services

- PropertyService
- ScoringService
- SettingsService
- ImportService
- ExportService
- PDFReportService
- MapExportService
- FileService

### Repositories

- PropertyRepository
- SettingRepository
- PriceHistoryRepository

## Design Direction

The UI should not perform business logic directly.

Good:

```python
self.property_service.recalculate_scores()
```

Bad:

```python
score = price * 0.3 + acreage * 0.2
```

Scoring, analysis, import rules, duplicate detection, and recommendations belong in services.

## Future Refactor

As the app grows, large files should be split:

```text
ui/property_workspace/
  property_workspace.py
  tabs/overview_tab.py
  tabs/listing_tab.py
  tabs/location_tab.py
  tabs/utilities_tab.py
  tabs/restrictions_tab.py
  tabs/financial_tab.py
  tabs/photos_tab.py
  tabs/documents_tab.py
  tabs/analysis_tab.py
```

This will keep the project easier to maintain.
