#!/bin/ash
echo "####################"
echo "## RUNNING TEST's ##"
echo "####################"

pip install -r requirements.txt
pip install coverage
coverage run manage.py test
coverage report --omit="*/test*,config/*,manage.py"
# coverage report html