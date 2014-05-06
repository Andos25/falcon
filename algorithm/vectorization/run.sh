#!/bin/bash

/home/hadoop/falcon/algorithm/vectorization/wordMark.py

/opt/hadoop/bin/hdfs dfs -mkdir /vectorinput
/opt/hadoop/bin/hdfs dfs -copyFromLocal ./fakeinput.txt /vectorinput
/opt/hadoop/bin/hdfs dfs -rm -r /vectoroutput

/opt/hadoop/bin/hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.2.0.jar -input /vectorinput/fakeinput.txt -output /vectoroutput -mapper /home/hadoop/falcon/algorithm/vectorization/vectorize_mapper.py -reducer /home/hadoop/falcon/algorithm/vectorization/vectorize_reducer.py 
