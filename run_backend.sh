#!/bin/sh
export PYTHONPATH="/app"
echo "Python path set as $PYTHONPATH"
echo "Backend migration"
python3.7 ./backend/manage.py migrate
echo "Running backend server"
python3.7 ./backend/manage.py runserver 0.0.0.0:8000 & python3.7 ./backend/manage.py time_spotter & python3.7 ./backend/manage.py slicer
echo "Backend ends"