#!/bin/bash

/opt/hadoop/bin/hdfs dfs -mkdir /input
/opt/hadoop/bin/hdfs dfs -copyFromLocal ./stopword /input
/opt/hadoop/bin/hdfs dfs -rm -r /output

/opt/hadoop/bin/hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.2.0.jar -input /input/stopword -output /output -mapper /home/hadoop/falcon/algorithm/tfidf/tfidf_mapper.py -reducer /home/hadoop/falcon/algorithm/tfidf/tfidf_reducer.py 

/opt/hadoop/bin/hdfs dfs -rm -r /output
