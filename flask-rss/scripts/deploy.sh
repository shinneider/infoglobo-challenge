#!/bin/ash

if [[ -z "${AWS_ACCESS_KEY_ID}" ]]; then
  echo "Need to set AWS_ACCESS_KEY_ID env"
  exit 1
fi

if [[ -z "${AWS_SECRET_ACCESS_KEY}" ]]; then
  echo "Need to set AWS_SECRET_ACCESS_KEY env"
  exit 1
fi

if [[ -z "${STAGE}" ]]; then
  echo "Need to set STAGE env"
  exit 1
fi

# create ambient and install li'bs
rm -rf venv
virtualenv venv -p python3
source venv/bin/activate
pip install -r requirements.txt
pip install zappa

# check if is a valid ambient
if [[ "$STAGE" =~ ^(develop|production)$ ]]; then
    # deploy to lambda 
    zappa update "$STAGE"
    deactivate
    exit 0
else
    echo "${STAGE} is not valid"
    deactivate
    exit 1
fi