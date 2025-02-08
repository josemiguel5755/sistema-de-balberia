#!/usr/bin/env bash
set -o errexit

# Actualiza pip
python -m pip install --upgrade pip

# Instala las dependencias
python -m pip install -r requirements.txt

# Configura Django
python manage.py collectstatic --no-input
python manage.py migrate