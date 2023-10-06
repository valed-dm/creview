#!/usr/bin/env bash

echo "Run collectstatic"
python manage.py collectstatic --no-input
