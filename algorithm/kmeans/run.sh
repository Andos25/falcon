#bin/bash

/opt/hadoop/bin/hadoop fs -rm /kmeansinput/clustercenter.txt
/opt/hadoop/bin/hadoop fs -put ./clustercenter.txt /kmeansinput

/opt/hadoop/bin/hadoop jar ./KMeans.jar
