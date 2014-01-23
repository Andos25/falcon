#!/bin/bash

#variables that you need to justify.
JAVA_NAME=java-7-oracle
USER_NAME=hduser
GROUP_NAME=hadoop
#hdfs namenode -format
#start-all.sh

#global vars 
DATA_TIME="$(date +'%d/%m/%Y')"
WORK_DIR=/usr/local
HADOOP_FILE=hadoop-2.2.0
#namenode and datanode install file
HADOOP_TEST_FILE=mydata
#configure file,you can change it to appropriate your need
CUR_USER_BASHRC=~/.bashrc


#Todo:check if ssh installed.
echo "install ssh..."	
apt-get install openssh-server
ssh-keygen -t rsa -P ""
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
echo "ssh install done.ssh version is:"
ssh -version
#ssh localhost

#begin to install    
#add by lane 2013-10-26
echo "hadoop install..."	
if [ ! -e ./${HADOOP_FILE} ]; then
	echo "Downloading hadoop, waitting..."	
	wgget -O $dir/${HADOOP_FILE}.tar.gz "mirror.esocc.com/apache/hadoop/common/${HADOOP_FILE}/${HADOOP_FILE}.tar.gz"
fi

rm -r ${WORK_DIR}/${HADOOP_FILE}
echo "Extracting ${HADOOP_FILE}..."
tar -xf ${HADOOP_FILE}.tar.gz -C ${WORK_DIR}/

#add by lane 2013-10-26
echo "Add ${HADOOP_FILE} path to ~/.bashrc file"
cp ${CUR_USER_BASHRC} ${CUR_USER_BASHRC}_bak
echo "" >> ${CUR_USER_BASHRC}
echo -e "#Add by hadoop, time:${DATA_TIME}" >> ${CUR_USER_BASHRC}
echo "export JAVA_HOME=/usr/lib/jvm/jdk" >> ${CUR_USER_BASHRC}
echo "export HADOOP_INSTALL=/usr/local/${HADOOP_FILE}" >> ${CUR_USER_BASHRC}
echo 'export HADOOP_CONF_DIR=$HADOOP_INSTALL/etc/hadoop' >> ${CUR_USER_BASHRC}
echo 'export PATH=$PATH:$HADOOP_INSTALL/bin' >> ${CUR_USER_BASHRC}
echo 'export PATH=$PATH:$HADOOP_INSTALL/sbin' >> ${CUR_USER_BASHRC}
source ${CUR_USER_BASHRC}

echo "modify ${WORK_DIR}/${HADOOP_FILE}/etc/hadoop/hadoop-env.sh"
cp hadoop-env.sh ${WORK_DIR}/${HADOOP_FILE}/etc/hadoop/hadoop-env.sh
source ${WORK_DIR}/${HADOOP_FILE}/etc/hadoop/hadoop-env.sh

echo "create namenode and datanode."
rm -r ${WORK_DIR}/mydata
mkdir -p ${WORK_DIR}/mydata/hdfs/namenode
mkdir -p ${WORK_DIR}/mydata/hdfs/datanode

echo "Configure Hadoop."
cp core-site.xml yarn-site.xml mapred-site.xml hdfs-site.xml ${WORK_DIR}/${HADOOP_FILE}/etc/hadoop
rm ${WORK_DIR}/${HADOOP_FILE}/etc/hadoop/mapred-site.xml.template

echo "change hadoop and mydata's ower."
sudo chmod 777 -R ${WORK_DIR}/${HADOOP_FILE}
sudo chmod 777 -R ${WORK_DIR}/mydata
sudo chown -R ${USER_NAME}:${GROUP_NAME} ${WORK_DIR}/mydata
sudo chown -R ${USER_NAME}:${GROUP_NAME} ${WORK_DIR}/${HADOOP_FILE}

#Todo:check if Java installed,if install check whether it's the least version.
echo "Do you want to update java?[y/n]"
read -p "Enter your choice : " choice
if [ "$choice" == "y" ]; then
	echo "java install/update..."	
	sudo add-apt-repository ppa:webupd8team/java
	sudo apt-get update
	sudo apt-get install openjdk-7-jdk
	cd /usr/lib/jvm && ln -s java-7-oracle jdk
	echo "java istall done.java version is:"
	java -version
fi
cd /usr/lib/jvm && ln -s ${JAVA_NAME} jdk
echo "hadoop install done!"

