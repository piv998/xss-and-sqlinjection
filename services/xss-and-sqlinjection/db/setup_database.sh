#!/usr/bin/env bash
# Wait for database to startup 
echo '!!!!!!!!!!!!!!!!! setup_database.sh STARTED !!!!!!!!!!!!!!!!!!'
sleep 60
echo '!!!!!!!!!!!!!!!!! 60 seconds were passed  !!!!!!!!!!!!!!!!'
./opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P "jo238jfieWIJr83r@^" -i setup.sql