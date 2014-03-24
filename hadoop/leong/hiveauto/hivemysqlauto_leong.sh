#!/bin/bash

HIVE_PATH=/opt
HIVE_TAR=hive-0.11.0.tar.gz
CONNECTOR=mysql-connector-java-5.1.18-bin.jar

#install mysql
if [ ! -e /etc/init.d/mysql ];then
sudo apt-get install mysql-server mysql-client
else
echo "mysql is already installed"
fi
sudo cp my.cnf /etc/mysql/my.cnf

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
if [ ! -e $HIVE_TAR ]; then
echo "downloading hive,please wait..."
wgget -O $HIVE_PATH/$HIVE_TAR "http://apache.dataguru.cn/hive/stable/hive-0.11.0.tar.gz"
fi
echo "extracting hive"
tar -zxvf $HIVE_TAR
mv hive-0.11.0 /opt
sudo chown -R hadoop:hadoop hive-0.11.0
#export hive path
sudo echo "export HIVE_HOME="${HIVE_PATH}/hive-0.11.0 >> /etc/profile
sudo echo "export PATH=$PATH:$HIVE_PATH/hive-0.11.0/bin" >> /etc/profile
cat /etc/profile
source /etc/profile

#copy mysql connection jar
sudo cp $CONNECTOR $HIVE_PATH/hive-0.11.0/lib
sudo chown hadoop:hadoop $HIVE_PATH/hive-0.11.0/lib/$CONNECTOR
#config hive
sudo cp hive-site.xml $HIVE_PATH/hive-0.11.0/conf/
sudo chown hadoop:hadoop $HIVE_PATH/hive-0.11.0/conf/hive-site.xml