# EVERLASTING BLOOM — Installation & Setup

## Requirements
- Python 3.10+
- pip

## Termux / Android
```bash
pkg install python sqlite
pip install flask
python app/app.py
```

## Ubuntu / Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install flask
python app/app.py
```

## CLI Companion (bloomctl)
```bash
python app/bloomctl version
python app/bloomctl letters
python app/bloomctl timeline
python app/bloomctl garden
```

## Admin Access
Set environment variable:
```bash
export EB_ADMIN_PASSWORD="your-secure-password"
```
Default (change immediately): `everbloom-admin-default-change`

## Unofficial Fan Project
EVERLASTING BLOOM is an unofficial tribute to White Lily Cookie. Not affiliated with Devsisters.
