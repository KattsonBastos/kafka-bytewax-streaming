# python -m bytewax.run -r db_dir/ cm-bytewax
# python -m bytewax.run dataflow --sqlite-directory . --epoch-interval 0
# python3 -m bytewax.run -r db_dir/ -s 1 -b 0 dataflow_w1

import datetime
from currency_converter import CurrencyConverter
from confluent_kafka import OFFSET_STORED

from bytewax.connectors.kafka import operators as kop, KafkaSourceMessage, KafkaSinkMessage
from bytewax import operators as op
from bytewax.dataflow import Dataflow

import json


## ---------- START: HELPER FUNCTIONS ---------- 

currency_converter = CurrencyConverter()

# Parse JSON records
def parse_json(record: KafkaSourceMessage) -> dict:
    value = record.value
    return json.loads(value)


# Filter records where spending is higher than 70
def filter_null_price(record):
    return record["price"] > 0

# miles to km convertion
def miles2km(record):
    m2km_value = 0.621371

    record['distance'] = float(round(record['distance']*m2km_value, 2))

    return record

# USD to BRL convertion
def usd2brl(record):
    record['price'] = currency_converter.convert(record['price'], 'USD', 'BRL')

    return record

# check if it is dynamic fare
def check_dynamic_fare(record):
    record['flag_dynamic_fare'] = False if record['surge_multiplier'] <= 1 else True

    return record


# add event time
def add_event_time(record):

    record['event_time'] = str(datetime.datetime.strptime(record['dt_current_timestamp'], "%Y-%m-%d %H:%M:%S.%f"))

    return record


# add processing time
def add_processing_time(record):
    record['processing_time'] = str(datetime.datetime.now())

    return record


# TODO: this is just for debugging purposes
def show_record(record): 

    print(record['user_id'])

    return None


# filter desired keys
def select_keys(record):

    key_list = [
        'user_id',
        'source',
        'destination',
        'flag_dynamic_fare',
        'price',
        'distance',
        'event_time', 
        'processing_time'
    ]

    record = {key: record[key] for key in key_list}

    return record

# Serialize records back to JSON
def serialize_json(record):
    return json.dumps(record).encode('utf-8')

## ---------- END: HELPER FUNCTIONS ---------- 


## ---------- START: DATAFLOW ---------- 
## printing just to make sure this script is running
print('Starting dataflow..')
# Kafka broker configuration
brokers = ["localhost:9092"]

# Define the dataflow
flow = Dataflow("treating_rides")

# Define the Kafka input
add_config = {
    "group.id": "bytewax_consumer", 
    "enable.auto.commit": "true", 
    "auto.commit.interval.ms": 1
}

kinp = kop.input(
    "kafka-in", 
    flow, 
    brokers=brokers, 
    topics=["input-raw-rides"],
    # batch_size=1,
    add_config = add_config,
    starting_offset=OFFSET_STORED,
)

event_parsed = op.map("parse_json", kinp.oks, parse_json)

event_filtered = event_parsed#op.filter("filter_null_price", event_parsed, filter_null_price)

event_transformed = op.map("miles2km", event_filtered, miles2km)
event_transformed = op.map("usd2brl", event_transformed, usd2brl)
event_transformed = op.map("add_processing_time", event_transformed, add_processing_time)
event_transformed = op.map("add_event_time", event_transformed, add_event_time)
event_transformed = op.map("check_dynamic_fare", event_transformed, check_dynamic_fare)
event_transformed = op.map("select_keys", event_transformed, select_keys)
_ = op.map("show_record", event_transformed, show_record) # TODO: this is just for debugging purposes

event_serialized = op.map("serialize_json", event_transformed, serialize_json)

# Define the Kafka output
event_processed = op.map("map_to_kafka_message", event_serialized, lambda x: KafkaSinkMessage(None, x))
kop.output("kafka-out", event_processed, brokers=brokers, topic="output-bytewax-enriched-rides")
## ---------- END: DATAFLOW ---------- 
## printing just to make sure this script is running
print('Dataflow running..')