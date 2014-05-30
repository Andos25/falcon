#bin/bash

#vectorization
/home/hadoop/falcon/algorithm/vectorization/vectorize_mapper.py | /home/hadoop/falcon/algorithm/vectorization/vectorize_reducer.py
python /home/hadoop/falcon/algorithm/kmeans/getCenter.py

/opt/hadoop-2.2.0/bin/hadoop fs -rm -r /kmeansinput
/opt/hadoop-2.2.0/bin/hadoop fs -mkdir /kmeansinput
/opt/hadoop-2.2.0/bin/hadoop fs -copyFromLocal /home/hadoop/kmeansdata/vector32w.txt /kmeansinput/vector.txt
/opt/hadoop-2.2.0/bin/hadoop fs -copyFromLocal /home/hadoop/kmeansdata/clustercenter32w.txt /kmeansinput/clustercenter.txt

/opt/hadoop-2.2.0/bin/hadoop jar /home/hadoop/falcon/algorithm/kmeans/KMeans.jar

rm /home/hadoop/kmeansdata/kmeansoutput32w.txt
/opt/hadoop-2.2.0/bin/hadoop fs -copyToLocal /kmeansoutput/part-r-00000 /home/hadoop/kmeansdata/kmeansoutput32w.txt
python /home/hadoop/falcon/algorithm/kmeans/keywordextract.py
