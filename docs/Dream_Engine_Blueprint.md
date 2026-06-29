# Dream Engine Blueprint

## Goal

The Dream Engine should explain why a property is good, risky, overpriced, underpriced, or worth watching.

## Score Categories

### Financial Score

Factors:

- Asking price
- Price per acre
- Estimated market value
- Estimated equity
- Site prep cost
- Taxes
- Offer room

### Location Score

Factors:

- Drive time to Gulf Shores
- Drive time to Foley
- Drive time to Fairhope
- Drive time to Pensacola
- Preferred city match
- Road type
- Paved road

### Utilities Score

Factors:

- Electric availability
- County water
- Public sewer
- Septic requirement
- Fiber
- Natural gas

### Flood / Land Risk Score

Factors:

- FEMA flood zone
- Wetlands
- Elevation
- Drainage concern
- Soil suitability

### Restrictions Score

Factors:

- No HOA
- HOA amount
- Shop allowed
- RV allowed
- Boat allowed
- Livestock allowed
- Barndominium allowed
- Mobile homes allowed

### Buildability Score

Factors:

- Road access
- Utilities
- Flood risk
- Wetlands
- Site prep estimate
- Shape/buildable area

### Market Opportunity Score

Future factors:

- Days on market
- Price drops
- Seller motivation
- Comparable sales
- Price versus comps

## Scoring Output

Each property should produce:

```text
Dream Score
Recommendation
Category Scores
Strengths
Weaknesses
Missing Data
Suggested Due Diligence
Suggested Offer
Negotiation Strength
```

## Avoiding Ties

Scores should use continuous calculations instead of broad buckets.

Examples:

- Price per acre should affect score continuously.
- Acreage should be scored based on distance from ideal acreage.
- Drive time should be scored continuously.
- HOA fee should penalize proportionally.
- Flood and wetlands should apply meaningful deductions.

## Missing Data

Missing data should not always be treated as neutral.

Examples:

- Unknown flood zone should lower confidence.
- Unknown utilities should reduce utility score.
- Unknown restrictions should reduce restrictions confidence.
- Missing GPS should disable map/location automation.

Future version should include a confidence score:

```text
Dream Score: 91.2
Confidence: 63%
```
