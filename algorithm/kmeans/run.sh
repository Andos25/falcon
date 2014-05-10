#bin/bash

/opt/hadoop-2.2.0/bin/hadoop fs -rm /kmeansinput/clustercenter.txt
/opt/hadoop-2.2.0/bin/hadoop fs -put ./clustercenter.txt /kmeansinput

/opt/hadoop-2.2.0/bin/hadoop jar ./KMeans.jar