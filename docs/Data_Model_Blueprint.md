# Data Model Blueprint

## Core Tables

### properties

Physical property record.

Important fields:

- address
- city
- county
- state
- zip_code
- parcel_number
- latitude
- longitude
- acres

### listings

Listing-specific information.

Important fields:

- source
- status
- asking_price
- mls_number
- url
- days_on_market

### price_history

Tracks price movement.

Important fields:

- listing_id
- price
- recorded_date
- note

### utilities

Utility availability.

Important fields:

- electric
- county_water
- public_sewer
- septic_required
- fiber
- natural_gas
- notes

### restrictions

HOA and use restrictions.

Important fields:

- hoa
- hoa_fee
- shop_allowed
- rv_allowed
- boat_allowed
- livestock_allowed
- mobile_home_allowed
- barndominium_allowed
- notes

### location_metrics

Location and risk metrics.

Important fields:

- minutes_to_gulf_shores
- minutes_to_foley
- minutes_to_fairhope
- minutes_to_pensacola
- flood_zone
- wetlands
- road_type
- paved_road

### financials

Financial estimates.

Important fields:

- estimated_market_value
- recommended_offer
- maximum_offer
- annual_taxes
- estimated_site_prep
- estimated_clearing
- estimated_driveway
- estimated_septic
- estimated_utilities

### score_components

Scoring outputs.

Important fields:

- price_score
- location_score
- utilities_score
- flood_score
- buildability_score
- restrictions_score
- dream_score
- negotiation_grade
- recommendation

### photos

Stored image references.

Important fields:

- file_path
- caption
- photo_type
- taken_date

### documents

Stored document references.

Important fields:

- file_path
- document_type
- notes

## Future Tables

### analysis_results

Stores generated property analysis.

Potential fields:

- property_id
- analysis_date
- overall_summary
- strengths_json
- weaknesses_json
- missing_data_json
- suggested_offer
- negotiation_strength
- recommendation

### comparable_sales

Stores comps.

Potential fields:

- property_id
- comp_address
- sale_price
- sale_date
- acres
- price_per_acre
- distance_miles
- source

### due_diligence_tasks

Tracks due-diligence checklist.

Potential fields:

- property_id
- task_name
- category
- status
- due_date
- notes

### saved_import_templates

Reusable import mappings.

Potential fields:

- name
- source_type
- mapping_json
