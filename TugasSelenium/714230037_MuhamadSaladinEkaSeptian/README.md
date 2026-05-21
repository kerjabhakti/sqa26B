# Commute Analyzer E2E Tests

## Requirements
- Python 3.11+
- Google Chrome (or Chromium)
- ChromeDriver (Selenium Manager can auto-download in most environments)

## Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run
```bash
pytest
```

## Headless
```bash
pytest --headless
```

## Override URLs
```bash
pytest --base-url https://commute.irc-enter.tech --api-url https://commute.irc-enter.tech/api/v1
```

## Device ID
```bash
E2E_DEVICE_ID=my-device-id pytest
```

## Artifacts
Failure screenshots and HTML snapshots are stored in `artifacts/`.
