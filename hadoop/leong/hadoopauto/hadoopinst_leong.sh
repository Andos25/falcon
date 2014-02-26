#!/bin/bash
#based on root user,in path /opt
HADOOP_PREFIX=/opt
HADOOP_CONFIG=${HADOOP_PREFIX}/hadoop-2.2.0/etc/hadoop/
JAVA_HOME=/usr/lib/jvm/java-7-openjdk-i386
HADOOP_TAR=/opt/hadoop-2.2.0.tar.gz
env=/etc/profile

#create hadoop user&group
sudo addgroup hadoop
sudo adduser --ingroup hadoop hadoop
#grant superuser privilege by copy file
sudo cp sudoers /etc/sudoers

#extract in /usr/local/lib
echo "extracting hadoop-2.2.0.tar.gz in /opt"
if [ ! -e $HADOOP_TAR ]; then
	echo "Downloading hadoop, waitting..."	
	wgget -O $HADOOP_TAR "mirrors.hust.edu.cn/apache/hadoop/common/hadoop-2.2.0/hadoop-2.2.0.tar.gz"
fi
sudo tar -zxvf $HADOOP_TAR
sudo chown hadoop:hadoop $HADOOP_TAR
#jdk install
echo "install jdk..."
sudo apt-get install openjdk-7-jdk
echo "jdk version is:"
java -version

#ssh install
echo "install ssh..."	
sudo apt-get install openssh-server
ssh-keygen -t rsa -P ""
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
echo "ssh install done.ssh version is:"
ssh -version

#config environment in /etc/profile
echo "config /etc/profile"
sudo echo "export JAVA_HOME="${JAVA_HOME} >> ${env}
sudo echo "export HADOOP_HOME=/opt/hadoop-2.2.0" >> ${env}
sudo echo "export PATH=$PATH:$JAVA_HOME/bin:$HADOOP_PREFIX/hadoop-2.2.0/sbin:$HADOOP_PREFIX/hadoop-2.2.0/bin" >> ${env}
source /etc/profile
cat /etc/profile

#config hadoop
sudo cp core-site.xml yarn-site.xml mapred-site.xml hdfs-site.xml hadoop-env.sh ${HADOOP_CONFIG}

echo "hadoop installation finished!"
