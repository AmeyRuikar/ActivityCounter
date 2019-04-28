from __future__ import print_function

import sys
import time
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils


# Function to create and setup a new StreamingContext
def functionToCreateContext(brokers, topic):

    sc = SparkContext(appName='ActivityCounts')  # new context
    ssc = StreamingContext(sc, 30)
    ssc.checkpoint('./checkpoint')  # set checkpoint directory

    kvs = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list": brokers})
    lines = kvs.map(lambda x: x[1])

    activity_counts = lines.map(lambda line: line.split('|')) \
                           .map(lambda rec: (rec[2], 1)) \
                           .reduceByKey(lambda a, b: a+b)
    activity_counts.pprint()

    running_acitivity_counts = activity_counts.updateStateByKey(updateFunc)
    running_acitivity_counts.pprint()

    return ssc


def updateFunc(new_value, running_value):

    if not running_value:
        running_value = 0
    
    return sum(new_value, running_value)


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print('Usage: direct_kafka_wordcount.py <broker_list> <topic>', file=sys.stderr)
        sys.exit(-1)
    
    brokers, topic = sys.argv[1:]

    ssc = StreamingContext.getOrCreate('./checkpoint', lambda: functionToCreateContext(brokers, topic))

    ssc.start()
    ssc.awaitTermination()   