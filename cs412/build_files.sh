#!/bin/bash

# Run Django collectstatic command
python manage.py collectstatic --noinput

# Move static files to the directory that Vercel will serve
mv staticfiles static