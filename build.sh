#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Ensure media directory exists (uses MEDIA_ROOT env var or local default)
mkdir -p "${MEDIA_ROOT:-media}"
