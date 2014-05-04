#!/bin/bash

/home/hadoop/falcon/algorithm/vectorization/wordMark.py

/opt/hadoop-2.2.0/bin/hdfs dfs -mkdir /vectorinput
/opt/hadoop-2.2.0/bin/hdfs dfs -copyFromLocal ./fakeinput.txt /vectorinput
/opt/hadoop-2.2.0/bin/hdfs dfs -rm -r /vectoroutput

/opt/hadoop-2.2.0/bin/hadoop jar /opt/hadoop-2.2.0/share/hadoop/tools/lib/hadoop-streaming-2.2.0.jar -input /vectorinput/fakeinput.txt -output /vectoroutput -mapper /home/hadoop/falcon/algorithm/vectorization/vectorize_mapper.py -reducer /home/hadoop/falcon/algorithm/vectorization/vectorize_reducer.py 