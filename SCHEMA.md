# Data Schema (Required Columns)

## Biweekly panel (CSV)
- `BiweekEnd` (datetime, ISO) — end timestamp for the 14-day bin
- `ReleaseWindowID` (int) — release window the biweek belongs to
- `y_defects` (int) — total defects in the bin
- `ActiveDevelopers` (int) — unique developers active in the bin

## Docinfo (CSV) for topic alignment demo
- `Bug ID` (string/int) — unique document/issue identifier
- `Topic` (int) — topic ID
