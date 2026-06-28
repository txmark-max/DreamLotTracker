# Dream Lot Tracker — Data Dictionary v1

## 1. properties

Core physical property record.

| Field | Type | Required | Notes |
|---|---|---:|---|
| id | integer | Yes | Primary key |
| parcel_number | text | No | County parcel ID |
| address | text | Yes | Street or descriptive address |
| city | text | Yes | City/community |
| county | text | Yes | County name |
| state | text | Yes | AL/FL/etc. |
| zip_code | text | No | ZIP code |
| latitude | real | No | GPS latitude |
| longitude | real | No | GPS longitude |
| acres | real | Yes | Lot size in acres |
| created_at | datetime | Yes | Record creation date |
| updated_at | datetime | Yes | Last update date |

## 2. listings

Listing-specific information.

| Field | Type | Required | Notes |
|---|---|---:|---|
| id | integer | Yes | Primary key |
| property_id | integer | Yes | FK to properties |
| mls_number | text | No | MLS number |
| source | text | No | Zillow/Realtor/MLS/manual |
| url | text | No | Listing link |
| agent | text | No | Listing agent |
| brokerage | text | No | Listing brokerage |
| status | text | Yes | Active/Pending/Sold/Watch/Off Market |
| asking_price | real | Yes | Current list price |
| list_date | date | No | Original list date |
| days_on_market | integer | No | DOM |
| created_at | datetime | Yes | Record creation date |
| updated_at | datetime | Yes | Last update date |

## 3. price_history

Tracks price changes over time.

| Field | Type | Required | Notes |
|---|---|---:|---|
| id | integer | Yes | Primary key |
| listing_id | integer | Yes | FK to listings |
| price | real | Yes | Recorded price |
| recorded_date | date | Yes | Date price was observed |
| note | text | No | Price drop, relist, manual update |

## 4. utilities

Utility availability.

| Field | Type | Required | Notes |
|---|---|---:|---|
| id | integer | Yes | Primary key |
| property_id | integer | Yes | FK to properties |
| electric | text | No | At road/Nearby/Unknown |
| county_water | text | No | Available/Unavailable/Unknown |
| well_required | boolean | No | True/False |
| public_sewer | text | No | Available/Unavailable/Unknown |
| septic_required | boolean | No | True/False |
| natural_gas | text | No | Available/Unavailable/Unknown |
| fiber | text | No | Available/Planned/Unavailable/Unknown |
| cable | text | No | Available/Unavailable/Unknown |
| notes | text | No | Utility notes |

## 5. restrictions

HOA and use restrictions.

| Field | Type | Required | Notes |
|---|---|---:|---|
| id | integer | Yes | Primary key |
| property_id | integer | Yes | FK to properties |
| hoa | text | No | None/Yes/Unknown |
| hoa_fee | real | No | Monthly or annual amount |
| hoa_fee_frequency | text | No | Monthly/Annual |
| minimum_home_sqft | integer | No | Minimum build size |
| shop_allowed | boolean | No | Detached shop/workshop |
| rv_allowed | boolean | No | RV parking allowed |
| boat_allowed | boolean | No | Boat parking allowed |
| livestock_allowed | boolean | No | Animals/livestock allowed |
| mobile_home_allowed | boolean | No | Mobile/manufactured homes |
| barndominium_allowed | boolean | No | Barndo allowed |
| short_term_rental_allowed | boolean | No | STR allowed |
| notes | text | No | Restriction notes |

## 6. location_metrics

Distances, flood risk, and site location data.

| Field | Type | Required | Notes |
|---|---|---:|---|
| id | integer | Yes | Primary key |
| property_id | integer | Yes | FK to properties |
| miles_to_gulf_shores | real | No | Distance |
| minutes_to_gulf_shores | integer | No | Drive time |
| minutes_to_foley | integer | No | Drive time |
| minutes_to_fairhope | integer | No | Drive time |
| minutes_to_pensacola | integer | No | Drive time |
| minutes_to_i10 | integer | No | Drive time |
| minutes_to_hospital | integer | No | Drive time |
| minutes_to_grocery | integer | No | Drive time |
| minutes_to_boat_launch | integer | No | Drive time |
| flood_zone | text | No | X/AE/VE/Unknown |
| wetlands | text | No | None/Possible/Confirmed/Unknown |
| road_type | text | No | County/Private/State/Unknown |
| paved_road | boolean | No | True/False |
| notes | text | No | Location notes |

## 7. financials

Cost and offer analysis.

| Field | Type | Required | Notes |
|---|---|---:|---|
| id | integer | Yes | Primary key |
| property_id | integer | Yes | FK to properties |
| estimated_market_value | real | No | Estimated FMV |
| recommended_offer | real | No | Suggested opening offer |
| maximum_offer | real | No | Ceiling price |
| annual_taxes | real | No | Property taxes |
| estimated_clearing | real | No | Clearing cost |
| estimated_driveway | real | No | Driveway cost |
| estimated_septic | real | No | Septic cost |
| estimated_utilities | real | No | Utility connection |
| estimated_site_prep | real | No | Total site prep |
| estimated_total_investment | real | No | Lot + prep |
| notes | text | No | Financial notes |

## 8. score_components

Stores individual category scores.

| Field | Type | Required | Notes |
|---|---|---:|---|
| id | integer | Yes | Primary key |
| property_id | integer | Yes | FK to properties |
| price_score | real | No | 0–100 |
| location_score | real | No | 0–100 |
| utilities_score | real | No | 0–100 |
| privacy_score | real | No | 0–100 |
| flood_score | real | No | 0–100 |
| buildability_score | real | No | 0–100 |
| appreciation_score | real | No | 0–100 |
| restrictions_score | real | No | 0–100 |
| investment_score | real | No | 0–100 |
| lifestyle_score | real | No | 0–100 |
| value_score | real | No | 0–100 |
| dream_score | real | No | Weighted total |
| negotiation_grade | text | No | A+ through D |
| recommendation | text | No | Dream Lot/Strong Buy/Watch/Pass |

## 9. notes

Freeform notes.

| Field | Type | Required | Notes |
|---|---|---:|---|
| id | integer | Yes | Primary key |
| property_id | integer | Yes | FK to properties |
| pros | text | No | Strengths |
| cons | text | No | Weaknesses |
| questions | text | No | Questions to ask |
| builder_notes | text | No | Build-related notes |
| visit_notes | text | No | Site visit notes |
| final_recommendation | text | No | Final decision |

## 10. comparable_sales

Nearby land sales.

| Field | Type | Required | Notes |
|---|---|---:|---|
| id | integer | Yes | Primary key |
| property_id | integer | Yes | FK to properties |
| comp_address | text | Yes | Comparable address |
| sale_price | real | Yes | Sale price |
| sale_date | date | No | Sale date |
| acres | real | No | Lot size |
| price_per_acre | real | No | Calculated |
| distance_miles | real | No | Distance from subject |
| source | text | No | MLS/county/manual |

## 11. photos

Photo references.

| Field | Type | Required | Notes |
|---|---|---:|---|
| id | integer | Yes | Primary key |
| property_id | integer | Yes | FK to properties |
| file_path | text | Yes | Local photo path |
| caption | text | No | Photo caption |
| photo_type | text | No | Listing/Drone/Street/Flood/GIS |
| taken_date | date | No | Date taken |

## 12. documents

Document references.

| Field | Type | Required | Notes |
|---|---|---:|---|
| id | integer | Yes | Primary key |
| property_id | integer | Yes | FK to properties |
| file_path | text | Yes | Local document path |
| document_type | text | No | Survey/Restrictions/Deed/FEMA/GIS |
| notes | text | No | Document notes |

## 13. watch_events

Tracks alerts and changes.

| Field | Type | Required | Notes |
|---|---|---:|---|
| id | integer | Yes | Primary key |
| property_id | integer | Yes | FK to properties |
| event_type | text | Yes | New Listing/Price Drop/Back Active/Status Change |
| event_date | datetime | Yes | Event date |
| old_value | text | No | Previous value |
| new_value | text | No | New value |
| note | text | No | Event notes |

## 14. settings

Application and scoring settings.

| Field | Type | Required | Notes |
|---|---|---:|---|
| key | text | Yes | Primary key |
| value | text | Yes | Stored setting value |
| description | text | No | Human-readable description |
