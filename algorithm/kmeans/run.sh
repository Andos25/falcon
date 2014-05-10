#bin/bash

/opt/hadoop/bin/hadoop fs -rm /kmeansinput/clustercenter.txt
/opt/hadoop/bin/hadoop fs -put /home/hadoop/falcon/algorithm/clustercenter.txt /kmeansinput

/opt/hadoop/bin/hadoop jar /home/hadoop/falcon/algorithm/KMeans.jar
