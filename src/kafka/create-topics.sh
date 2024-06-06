#!bin/bash

kafka-topics --create --topic=users --bootstrap-server=localhost:9092 --partitions=3

kafka-topics --create --topic=users-high-spending --bootstrap-server=localhost:9092 --partitions=3

kafka-console-consumer --bootstrap-server=localhost:9092 --topic=users-high-spending 