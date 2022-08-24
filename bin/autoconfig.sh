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
echo "Access your mysql user with privileges for create a new user:";
echo "Your user:";
read root_user;
mysql -u $root_user -p < autoconfig.sql;
rm autoconfig.sql;
echo "MYSQL_CONFIG = {\"user\": \"$user\", \"password\": \"$password\", \"host\": \"$host\", \"database\": \"keylogger\"}" > .env;

# Set directory of libs
echo "PYTHONPATH='lib/'" >> .env

# Config autostart
path="${PWD}/bin/runner.py";
echo "#!/bin/sh" > start_keylogger.sh;
echo "exec pipenv shell & sudo pipenv run python3 $path & exit &" >> start_keylogger.sh;

chmod +x start_keylogger.sh;
shc -f start_keylogger.sh -o keylogger;
rm start_keylogger.sh;
sudo mv keylogger /bin/;
sudo mv keylogger.service /etc/systemd/system/;
systemctl enable keylogger.service;
systemctl start keylogger.service;

echo "Keylogger status: $(systemctl is-active keylogger.service)";
