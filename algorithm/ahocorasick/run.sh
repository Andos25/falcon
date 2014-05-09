#!/bin/bash

/opt/hadoop/bin/hdfs dfs -mkdir /input
/opt/hadoop/bin/hdfs dfs -copyFromLocal ./mapper.py /input
/opt/hadoop/bin/hdfs dfs -rm -r /output

/opt/hadoop/bin/hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.2.0.jar -input /input/mapper.py -output /output -mapper /home/hadoop/falcon/algorithm/ahocorasick/mapper.py -reducer /home/hadoop/falcon/algorithm/ahocorasick/reducer.py 

/opt/hadoop/bin/hdfs dfs -rm -r /output
