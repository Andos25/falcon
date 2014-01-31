#!/bin/bash

$HIVE_PATH=/usr/local/lib
$HIVE_TAR=hive-0.11.0.tar.gz
#install mysql
ps aux | grep mysql >/dev/null 2>&1
if [ $? -ne 0 ];then
	sudo apt-get install mysql-server mysql-client
else
	echo "mysql is already installed"
fi
cp my.cnf /etc/mysql/my.cnf

#create user and db for hive
echo "creating mysql user and db for hive"
mysql -uroot -p1 -e"
create user hive@'localhost' identified by 'hive';
grant all privileges on *.* to hive@localhost with grant option;
flush privileges;
use mysql;
select host,user from user;"
mysql -uhive -phive -e"
create database metahive;
show databases;
use metahive;
show tables;"

#extract hive
echo "extracting hive"
if [ -a $hive_TAR ]; then
        tar -zxvf Hive_TAR
fi
mv hive-0.11.0 HIVE_PATH

#export hive path
echo "export HIVE_HOME="${HIVE_PATH}/hive-0.11.0 >> /etc/profile
echo "export PATH=.:$HIVE_PATH/bin" >> /etc/profile

#copy mysql connection jar
cp mysql-connector-java-5.1.18-bin.jar $HIVE_PATH/hive-0.11.0/lib

#config hive
cp hive-site.xml HIVE_PATH/conf/
