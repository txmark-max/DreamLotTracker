# Property Analyzer Blueprint

## Goal

The analyzer should answer:

> Why should I buy or pass on this property?

## Analysis Sections

### Overall Recommendation

Examples:

- Dream Lot
- Strong Buy
- Watch List
- Pass
- Missing Critical Data

### Summary

A short plain-English explanation.

Example:

```text
This property is a strong candidate because it is under your price cap, close to your ideal acreage, has no known HOA, and is in a preferred city. The main concern is that utility availability and flood status are not fully verified.
```

### Strengths

Examples:

- Under max price
- Good price per acre
- Preferred city
- No HOA
- Fiber available
- Outside known flood zone
- Good acreage fit

### Weaknesses

Examples:

- Flood zone AE
- Septic required
- Unknown utility status
- HOA present
- Price above target
- Too far from Gulf Shores

### Missing Data

Examples:

- GPS coordinates missing
- Flood zone unknown
- Utility status unknown
- Restrictions not verified
- Taxes missing
- Parcel number missing

### Suggested Due Diligence

Examples:

- Verify county water availability
- Confirm septic feasibility
- Pull FEMA flood panel
- Check county GIS parcel map
- Ask for survey
- Ask for recorded restrictions
- Check driveway permit requirements

### Suggested Offer

Future version should calculate:

```text
Recommended Offer
Maximum Offer
Negotiation Strength
```

Inputs:

- Asking price
- Price per acre
- Estimated market value
- Site prep costs
- Price history
- Days on market
- Comparable sales

## Analysis Service Design

Future service:

```python
class AnalysisService:
    def analyze_property(property_id: int) -> PropertyAnalysis:
        ...
```

Output object:

```python
PropertyAnalysis(
    summary=str,
    strengths=list[str],
    weaknesses=list[str],
    missing_data=list[str],
    due_diligence=list[str],
    suggested_offer=float,
    maximum_offer=float,
    negotiation_strength=str,
)
```
