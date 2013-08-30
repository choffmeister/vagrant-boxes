#!/usr/bin/env bash
apt-get update

## ============================================
## Settings
## ============================================

MYSQL_ROOT_PASSWORD="root"

## ============================================
## Install Apache2, MySQL and PHP5
## ============================================

# set MySQL root password to root
echo debconf mysql-server/root_password password $MYSQL_ROOT_PASSWORD | debconf-set-selections
echo debconf mysql-server/root_password_again password $MYSQL_ROOT_PASSWORD | debconf-set-selections

# install Apache, MySQL and PHP5
apt-get install -y apache2 php5 php5-mysql mysql-server
a2enmod rewrite
service apache2 restart

# make MySQL listen on all devices
sed -i /etc/mysql/my.cnf -e 's/127\.0\.0\.1/0\.0\.0\.0/g'
service mysql restart

# install common used extensions
aptitude install -y php5-intl php-apc php5-xdebug

## ============================================
## Install PEAR
## ============================================

# install PEAR
aptitude install -y php-pear

## ============================================
## Install PHPUnit and PHP_CodeCoverage and PHP_Sniffer
## ============================================

# install PHPUnit and PHP_CodeCoverage
pear config-set auto_discover 1
pear channel-discover pear.phpunit.de
pear channel-discover components.ez.no
pear install --alldeps pear.phpunit.de/PHPUnit
pear install --alldeps phpunit/PHP_CodeCoverage

# install PHP_CodeSniffer
pear install --alldeps PHP_CodeSniffer

## ============================================
## Install Composer
## ============================================

curl -sS https://getcomposer.org/installer | php
mv composer.phar /usr/local/bin/composer
