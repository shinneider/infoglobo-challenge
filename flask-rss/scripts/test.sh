#!/bin/ash
echo "####################"
echo "## RUNNING TEST's ##"
echo "####################"

pip install -r requirements.txt
pip install pytest coverage pytest-cov
py.test
pytest --cov-report html --cov=app ./
pytest --cov=app ./