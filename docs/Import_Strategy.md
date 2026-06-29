# Import Strategy

## Current Import

Current import supports CSV and Excel with these fields:

- address
- city
- county
- state
- price
- acres
- status
- latitude
- longitude

## Near-Term Improvements

### Field Mapping

Allow user to map columns.

Example:

```text
Listing Price -> price
Lot Size -> acres
Town -> city
```

### Import Preview

Show:

- Valid rows
- Missing required fields
- Duplicate rows
- Rows that will be skipped
- Rows that need mapping

### Duplicate Detection

Current duplicate detection is address + city.

Future duplicate detection should use:

- Parcel number
- Address + city
- GPS proximity
- MLS number
- URL

### Import Templates

Save mappings by source.

Examples:

- Zillow export
- Realtor.com export
- MLS CSV
- County GIS CSV

### Post-Import Actions

After import:

- Recalculate scores
- Add import batch record
- Show import report
- Flag missing data
- Create due-diligence tasks

## Long-Term Import Ideas

- Listing URL parser
- County GIS parcel import
- Tax assessor import
- FEMA flood import
- Google Maps/drive-time enrichment
