#!/bin/bash

# Config mysql database and env variables
echo 'Define you user for keylogger database: ';
read user;
echo 'Define you password for keylogger database: ';
read password;
echo 'How is the mysql host: ';
read host;

echo "CREATE DATABASE IF NOT EXISTS keylogger;" > autoconfig.sql
echo "CREATE USER IF NOT EXISTS '$user'@'$host' IDENTIFIED BY '$password';" >> autoconfig.sql;
echo "GRANT ALL PRIVILEGES ON keylogger.* TO '$user'@'$host';" >> autoconfig.sql;
clear;
echo "Access your sql to run configs:";
mysql -u root -p < autoconfig.sql
echo "MYSQL_CONFIG = {\"user\": \"$user\", \"password\": \"$password\", \"host\": \"$host\", \"database\": \"keylogger\"}" > .env;
