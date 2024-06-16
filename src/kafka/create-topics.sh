#!bin/bash

kafka-topics --create --topic=input-raw-rides --bootstrap-server=localhost:9092 --partitions=3 --replication-factor=1

kafka-topics --create --topic=output-bytewax-enriched-rides --bootstrap-server=localhost:9092 --partitions=3  --replication-factor=1

kafka-console-consumer --bootstrap-server=localhost:9092 --topic=output-bytewax-enriched-rides