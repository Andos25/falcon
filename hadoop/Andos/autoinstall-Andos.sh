#!/bin/bash

#settings !!! before you using, you must set line 4 to 8
HADOOP_PREFIX=/opt
JAVA_HOME=/usr/lib/jvm/java-7-openjdk-i386
USER_NAME=hadoop
GROUP_NAME=hadoop
HADOOP_TAR=~/hadoop-2.2.0.tar.gz
CUR_USER_BASHRC=~/.bashrc
PROFILE=/etc/profile
sudo chmod 777 -R ${HADOOP_PREFIX}
sudo apt-get installl openjdk-7-jdk
#extract
echo "extracting"
if [ -a ${HADOOP_PREFIX}/hadoop ];then
    rm -r ${HADOOP_PREFIX}/hadoop
fi
if [ ! -a hadoop-2.2.0 ];then
    tar zxvf $HADOOP_TAR
fi
#mv hadoop-2.2.0 hadoop
mv hadoop-2.2.0 ${HADOOP_PREFIX}/hadoop


#create keygen
sudo apt-get install ssh
if [ -a ~/.ssh ];then
    rm -r ~/.ssh
fi
ssh-keygen -t rsa -P ""
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys



#configure env
echo "Add ${HADOOP_FILE} path to ~/.bashrc file"
echo "export HADOOP_PREFIX="${HADOOP_PREFIX} >> ${CUR_USER_BASHRC} 
echo "export JAVA_HOME="${JAVA_HOME} >> ${CUR_USER_BASHRC}
echo "PATH=$HADOOP_PREFIX/hadoop/bin:$HADOOP_PREFIX/hadoop/sbin:$JAVA_HOME/bin" >> ${CUR_USER_BASHRC}
echo "export HADOOP_MAPRED_HOME=${HADOOP_PREFIX}/hadoop/share/mapred" >> ${CUR_USER_BASHRC}      
echo "export HADOOP_COMMON_HOME=${HADOOP_PREFIX}/hadoop/share/common" >> ${CUR_USER_BASHRC}      
echo "export HADOOP_HDFS_HOME=${HADOOP_PREFIX}/hadoop/share/hdfs" >> ${CUR_USER_BASHRC}      
echo "export YARN_HOME=${HADOOP_PREFIX}/hadoop/share/yarn" >> ${CUR_USER_BASHRC} 
echo "export HADOOP_CONF_DIR=${HADOOP_PREFIX}/etc/hadoop" >> ${CUR_USER_BASHRC}
echo "export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-i386" >> ${CUR_USER_BASHRC}
echo "export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:JAVA_HOME/lib/tools.jar" >> ${CUR_USER_BASHRC}
source ${CUR_USER_BASHRC}

#configure
cp hadoop-env.sh ${HADOOP_PREFIX}/hadoop/etc/hadoop/hadoop-env.sh
source ${HADOOP_PREFIX}/hadoop/etc/hadoop/hadoop-env.sh

echo "create namenode and datanode."
if [ -a ${HADOOP_PREFIX}/mydata ]; then
    rm -r ${HADOOP_PREFIX}/mydata
fi
sudo mkdir -p /home/hadoop/dfs/name
sudo mkdir -p /home/hadoop/dfs/data

cp core-site.xml yarn-site.xml mapred-site.xml hdfs-site.xml ${HADOOP_PREFIX}/hadoop/etc/hadoop

sudo chmod 777 -R ${HADOOP_PREFIX}/hadoop
sudo chmod 777 -R /home/hadoop/dfs
sudo chown -R ${USER_NAME}:${GROUP_NAME} /home/hadoop/dfs
sudo chown -R ${USER_NAME}:${GROUP_NAME} ${HADOOP_PREFIX}/hadoop
echo "finished"

