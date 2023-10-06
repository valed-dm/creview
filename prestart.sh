#!/usr/bin/env bash

echo "Running migrations, run collectstatic"
python manage.py collectstatic --no-input
