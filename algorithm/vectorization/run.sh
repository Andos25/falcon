#!bin/bash

python /home/hadoop/falcon/algorithm/vectorization/wordMark.py

/home/hadoop/falcon/algorithm/vectorization/vectorize_mapper.py | /home/hadoop/falcon/algorithm/vectorization/vectorize_reducer.py