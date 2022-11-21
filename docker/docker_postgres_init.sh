#!/bin/bash
# set -e
# echo $POSTGRES_USER
# echo $POSTGRES_PASSWORD
# psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<-EOSQL
#     CREATE USER  stocks WITH PASSWORD 'stocks' CREATEDB;
#     CREATE DATABASE stocks
#         WITH 
#         OWNER = stocks
#         ENCODING = 'UTF8'
#         LC_COLLATE = 'en_US.utf8'
#         LC_CTYPE = 'en_US.utf8'
#         TABLESPACE = pg_default
#         CONNECTION LIMIT = -1;
# EOSQL

# creates new db and new user who is owner of this db
# arg1 db name
# arg2 user name
# arg3 user pass
create_db_user_pass() {
    psql --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -c "CREATE USER $2 WITH PASSWORD '$3'" && \
    psql --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -c "CREATE DATABASE $1 OWNER=$2"
 }

create_db_user_pass $DB_USER       $DB_USER          $DB_USER