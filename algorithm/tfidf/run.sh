#!/bin/bash

/opt/hadoop-2.2.0/bin/hdfs dfs -mkdir /tfidfinput
/opt/hadoop-2.2.0/bin/hdfs dfs -copyFromLocal /home/hadoop/falcon/algorithm/tfidf/stopword /tfidfinput
/opt/hadoop-2.2.0/bin/hdfs dfs -rm -r /tfidfoutput

/opt/hadoop-2.2.0/bin/hadoop jar /opt/hadoop-2.2.0/share/hadoop/tools/lib/hadoop-streaming-2.2.0.jar -input /tfidfinput/stopword -output /tfidfoutput -mapper /home/hadoop/falcon/algorithm/tfidf/tfidf_mapper.py -reducer /home/hadoop/falcon/algorithm/tfidf/tfidf_reducer.py 
