#!/bin/bash

# Config mysql database and env variables
echo 'Define you user for keylogger database: ';
read user;
echo 'Define you password for keylogger database: ';
read -s password;
echo 'How is the mysql host: ';
read host;

# Generate autoconfig.sql
echo "
CREATE DATABASE IF NOT EXISTS keylogger;
USE keylogger;
CREATE TABLE IF NOT EXISTS keyboard_key (
	name VARCHAR(16) NOT NULL,
	count INT NOT NULL,
	date DATE NOT NULL
);
CREATE USER IF NOT EXISTS '$user'@'$host' IDENTIFIED BY '$password';
GRANT ALL PRIVILEGES ON keylogger.* TO '$user'@'$host';
" > autoconfig.sql;

clear;
echo "Access your sql to run configs:";
mysql -u root -p < autoconfig.sql;
rm autoconfig.sql;
echo "MYSQL_CONFIG = {\"user\": \"$user\", \"password\": \"$password\", \"host\": \"$host\", \"database\": \"keylogger\"}" > .env;