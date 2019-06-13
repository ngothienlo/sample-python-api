#!/usr/bin/env bash
echo "Install required packages"


# install python
sudo apt-get update
sudo apt-get install build-essential python-pip libffi-dev python-dev python3-dev libpq-dev

# install postgres
apt-get install -y postgresql

sudo cp ./db_conf/* /etc/postgresql/11/main

# echo "CREATE ROLE deploy LOGIN ENCRYPTED PASSWORD '$APP_DB_PASS';" | sudo -u postgres psql
sudo -u postgres bash -c "psql -c \"CREATE USER assign_user WITH PASSWORD 'assign_123';\""
sudo su postgres -c "createdb assignment_api --owner assign_user"
service postgresql reload



# check venv
type virtualenv >/dev/null 2>&1 || { echo >&2 "No suitable python virtual env tool found, aborting"; exit 1; }

# create venv for app
rm -rf .demo_api
virtualenv -p python3 .demo_api
source .demo_api/bin/activate
pip install -r requirements.txt

source .demo_api/bin/activate
python3 ./app/models.py


echo "Install required packages finished"