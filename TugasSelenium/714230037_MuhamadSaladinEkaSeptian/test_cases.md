# E2E Test Cases

## Scope
These test cases validate critical user journeys for Commute Analyzer. They are grouped by suite and intended execution cadence.

## Smoke Suite

### SMK-01 App loads and map renders
- Preconditions: App is accessible.
- Steps:
  1. Open the app.
  2. Wait for the app title to appear.
  3. Wait for the map container to appear.
- Expected:
  - App title visible.
  - Map container visible.

### SMK-02 Create commute (happy path)
- Preconditions: No existing commutes for test device.
- Steps:
  1. Open the app.
  2. Click add commute.
  3. Enter commute name.
  4. Pick home and office on map.
  5. Choose vehicle, fuel price, and days per week.
  6. Submit.
- Expected:
  - Commute list shows the new commute.

### SMK-03 Delete commute
- Preconditions: At least one commute exists.
- Steps:
  1. Delete the commute from list.
- Expected:
  - Empty state is displayed.

## Regression Suite

### REG-01 Update commute
- Preconditions: At least one commute exists.
- Steps:
  1. Open edit for the first commute.
  2. Update name, vehicle, fuel price, and days per week.
  3. Submit.
- Expected:
  - Commute list shows updated values.

### REG-02 Route outputs render
- Preconditions: At least one commute exists.
- Steps:
  1. Create a commute.
  2. Verify annual cost and annual workdays are shown.
- Expected:
  - Annual cost is displayed.
  - Annual workdays text is displayed.

## Negative/Edge Suite

### NEG-01 Submit disabled until required inputs
- Preconditions: None.
- Steps:
  1. Open add commute form.
  2. Observe submit button.
- Expected:
  - Submit button is disabled until both points are selected.
