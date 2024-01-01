#!/bin/ash

# Secure entrypoint
chmod 600 /entrypoint.sh

# Initialize & Start MariaDB
mkdir -p /run/mysqld
chown -R mysql:mysql /run/mysqld
mysql_install_db --user=mysql --ldata=/var/lib/mysql
mysqld --user=mysql --console --skip-networking=0 &

# Wait for mysql to start
while ! mysqladmin ping -h'localhost' --silent; do echo 'not up' && sleep .2; done

# Populate database
mysql -u root << EOF
CREATE DATABASE spellbound_servant;
CREATE TABLE spellbound_servant.users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username varchar(255) NOT NULL UNIQUE,
    password varchar(255) NOT NULL
);

CREATE USER 'xclow3n'@'localhost' IDENTIFIED BY 'xclow3n';
GRANT SELECT, INSERT, UPDATE ON spellbound_servant.users TO 'xclow3n'@'localhost';
FLUSH PRIVILEGES;
EOF


/usr/bin/supervisord -c /etc/supervisord.conf