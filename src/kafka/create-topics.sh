#!bin/bash

kafka-topics --create --topic=rides --bootstrap-server=localhost:9092 --partitions=3

kafka-topics --create --topic=rides-refined --bootstrap-server=localhost:9092 --partitions=3

kafka-console-consumer --bootstrap-server=localhost:9092 --topic=rides-refined