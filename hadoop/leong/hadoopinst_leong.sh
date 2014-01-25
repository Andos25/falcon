#!/bin/bash
#bases on hadoop user
HADOOP_PREFIX=/usr/local/lib
HADOOP_CONFIG=${HADOOP_PREFIX}/hadoop-2.2.0/etc/hadoop/
JAVA_HOME=/usr/lib/jvm/java-7-openjdk-i386
USER_NAME=hadoop
USER_GROUP_NAME=hadoop
HADOOP_TAR=/user/local/lib/hadoop-2.2.0.tar.gz
env=/etc/profile

#extract in /usr/local/lib
echo "extracting hadoop-2.2.0.tar.gz in /usr/local/lib"
#if dir hadoop exits,then remove it
if [ -d ${HADOOP_PREFIX}/hadoop ]; then
	sudo rm -f ${HADOOP_PREFIX}/hadoop
fi
if [ -a $HADOOP_TAR ]; then
	tar -zxvf HADOOP_TAR
fi
sudo mv hadoop-2.2.0 ${HADOOP_PREFIX}
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
sudo echo "export HADOOP_HOME=/usr/local/lib/hadoop-2.2.0" >> ${env}
sudo echo "export PATH=$PATH:$JAVA_HOME/bin:$HADOOP_HOME/sbin:$HADOOP_HOME/bin" >> ${env}

#config hadoop
sudo cp core-site.xml yarn-site.xml mapred-site.xml hdfs-site.xml hadoop_env.sh ${HADOOP_CONFIG}

echo "hadoop installation finished!"
