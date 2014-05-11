#bin/bash

#vectorization
../vectorization/vectorize_mapper.py | ../vectorization/vectorize_reducer.py

/opt/hadoop-2.2.0/bin/hadoop fs -mkdir /kmeansinput
/opt/hadoop-2.2.0/bin/hadoop fs -rm /kmeansinput/vector.txt
/opt/hadoop-2.2.0/bin/hadoop fs -put /home/hadoop/falcon/algorithm/vectorization/vector.txt /kmeansinput
/opt/hadoop-2.2.0/bin/hadoop fs -rm /kmeansinput/clustercenter.txt
/opt/hadoop-2.2.0/bin/hadoop fs -put ./clustercenter.txt /kmeansinput

/opt/hadoop-2.2.0/bin/hadoop jar ./KMeans.jar

/opt/hadoop-2.2.0/bin/hadoop fs -copyToLocal /kmeansoutput/part-r-00000 /home/hadoop/falcon/algorithm/kmeans/
./keywordextract.py