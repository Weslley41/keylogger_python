#!/bin/bash

# Check dependencies
# from https://stackoverflow.com/a/52552095
echo -n "Checking dependencies... "
for name in python3 mysql pipenv
do
  [[ $(which $name 2>/dev/null) ]] || { echo -en "\n$name needs to be installed.";deps=1; }
done
[[ $deps -ne 1 ]] && echo "OK" || { echo -en "\nInstall the above and rerun this script\n";exit 1; }

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
echo "Config mysql database...";
echo "Access your mysql user with privileges for create a new user:";
echo "Your user:";
read root_user;
mysql -u $root_user -p < autoconfig.sql;
rm autoconfig.sql;

echo "Set environment variables";
echo "MYSQL_CONFIG={\"user\": \"$user\", \"password\": \"$password\", \"host\": \"$host\", \"database\": \"keylogger\"}" > .env;
echo "PYTHONPATH='lib/'" >> .env

# Install python dependencies
echo "Install python dependencies...";
sudo pipenv sync;

# Config autostart
echo "Config autostart service...";
echo "
[Unit]
Description=Keylogger

[Service]
RemainAfterExit=yes
User=root
WorkingDirectory=${PWD}
ExecStart=sudo pipenv run python3 bin/runner.py

[Install]
WantedBy=multi-user.target
" > keylogger.service;

sudo mv keylogger.service /etc/systemd/system/;
sudo systemctl enable --now keylogger.service;

echo "Finish";
echo "check: systemctl status keylogger.service";
