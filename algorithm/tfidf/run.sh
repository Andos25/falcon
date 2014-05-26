#!/bin/bash

/opt/hadoop/bin/hdfs dfs -mkdir /tfidfinput
/opt/hadoop/bin/hdfs dfs -copyFromLocal /home/hadoop/falcon/algorithm/tfidf/stopword /tfidfinput
/opt/hadoop/bin/hdfs dfs -rm -r /tfidfoutput

/opt/hadoop/bin/hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.2.0.jar -input /tfidfinput/stopword -output /tfidfoutput -mapper /home/hadoop/falcon/algorithm/tfidf/tfidf_mapper.py -reducer /home/hadoop/falcon/algorithm/tfidf/tfidf_reducer.py 
