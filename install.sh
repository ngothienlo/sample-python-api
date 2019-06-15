#!/usr/bin/env bash
echo "Install required packages"


# install python
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -sc)-pgdg main" > /etc/apt/sources.list.d/PostgreSQL.list'
sudo apt-get update
sudo apt-get install build-essential python-pip libffi-dev python-dev python3-dev libpq-dev

# install postgres 11
sudo apt-get install postgresql-11
sudo cp ./db_conf/* /etc/postgresql/11/main
sudo pg_ctlcluster 11 main start

useradd postgres
chown "postgres" /usr/local/pgsql
mkdir /usr/local/pgsql/data
chown postgres:postgres /usr/local/pgsql/data
sudo -u postgres bash -c "psql -c \"CREATE USER assign_user WITH PASSWORD 'assign_123';\""
sudo su postgres -c "createdb assignment_api --owner assign_user"
service postgresql reload


sudo apt install virtualenv
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