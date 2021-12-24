#!/usr/bin/env bash
# Wait for database to startup 
echo '!!!!!!!!!!!!!!!!! setup_database.sh STARTED !!!!!!!!!!!!!!!!!!'
sleep 100
echo '!!!!!!!!!!!!!!!!! 100 seconds were passed  !!!!!!!!!!!!!!!!'
./opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P "jo238jfieWIJr83r@^" -i setup.sql