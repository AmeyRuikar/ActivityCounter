# ActivityCounter

## Setup
To setup this project you will need two keep pieces:

1. Apache Spark
2. Apache Kafka

Here is a quick setup guide for both of these projects:

1. Apache Spark: [2.3.3](https://spark.apache.org/releases/spark-release-2-3-3.html)
You can download a `tar` package with version 2.3.3 - [here](https://spark.apache.org/downloads.html). Once you have the `tar`, you can extract it with the following command and you will be ready with `Spark` setup.
> $ tar -xvf ~/Downloads/spark-2.3.3-bin-hadoop2.7.tgz 

2. Apache Kafka: [2.12-2.2.0](https://kafka.apache.org/quickstart)
Similar to #1, you can get a `tar` package from this [location](https://kafka.apache.org/downloads). In this example we'll be using Kafka version 2.2.0 and one which is packaged with `scala 2.12`. Follow the next steps to setup Kafka. 

Note: Apache Kafka requires a `Zookeeper` node, so we will instantiate one, it comes pre-packed within the Kafka `tar`.

Steps:

> tar -xzf kafka_2.12-2.2.0.tgz

> cd kafka_2.12-2.2.0

> bin/zookeeper-server-start.sh config/zookeeper.properties #start the zookeeper

> bin/kafka-server-start.sh config/server.properties # start the kafka server

> bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic activity_test  # create a topic

> bin/kafka-topics.sh --list --bootstrap-server localhost:9092 # check if the topics was created

> bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning # start a sample consumer

With this all the installations are complete.

## Running the app
First, we need to generate log records and send them to Kafka. Inorder to simulate random traffic, use the `produce_kakfa_records.py` script. This script will generate records in the form of `time|user_id|activity` and post them to kafka. To setup the part you can create a `virtualenv` and download the `kafka-python` client. You need to have Kafka running before you do this step. To start the script:
> python produce_kafka_records.py

Next, we need to submit a `Spark Streaming` job to our spark installation. 

`cd` to the location of *spark-2.3.3-bin-hadoop2.7* and submit the following command:

> bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8-assembly_2.11:2.3.3 ~/Documents/git/ActivityCounter/activity_counts.py localhost:9092 activity_test

This will start consuming records from the kafka and start aggregating count for various activities. You can see sample output in the console.

```
-------------------------------------------
Time: 2019-04-27 19:09:30
-------------------------------------------
('interested', 2652)
('login', 2760)
('like', 2700)
('shared', 2795)
('tagged', 2758)
('status', 2659)
('going', 2605)
('comment', 2656)

```



