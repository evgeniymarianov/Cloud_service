#!/bin/bash

set -e

echo "${0}: running migrations."
python3 manage.py migrate

echo "${0}: start loaddata"
python3 manage.py loaddata data1.json

exec "$@"
