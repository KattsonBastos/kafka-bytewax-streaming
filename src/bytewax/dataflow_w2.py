#python -m bytewax.run cm-bytewax

import datetime
from currency_converter import CurrencyConverter
from confluent_kafka import OFFSET_STORED

from bytewax.connectors.kafka import operators as kop, KafkaSinkMessage
from bytewax import operators as op
from bytewax.dataflow import Dataflow

import json


## HELPER FUNCTIONS

currency_converter = CurrencyConverter()

# Parse JSON records
def parse_json(record):
    value = record.value
    return json.loads(value)


# Filter records where spending is higher than 70
def filter_null_price(record):
    return record["price"] > 0


def miles2km(record):
    m2km_value = 0.621371

    record['distance'] = float(round(record['distance']*m2km_value, 2))

    return record


def usd2brl(record):
    record['price'] = currency_converter.convert(record['price'], 'USD', 'BRL')

    return record


def check_dynamic_fare(record):
    record['flag_dynamic_fare'] = False if record['surge_multiplier'] <= 1 else True

    return record


def add_processing_time(record):
    record['dt_processing_timestamp'] = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S%f")

    return record

# TODO: this is just for debugging purposes
def show_record(record): 

    print(record['user_id'])

    return record


# Serialize records back to JSON
def serialize_json(record):
    return json.dumps(record).encode('utf-8')
## ------


print('Starting dataflow..')
# Kafka broker configuration
brokers = ["localhost:9092"]

# Define the dataflow
flow = Dataflow("terating_rides2")

# Define the Kafka input
add_config = {"group.id": "consumer_group", "enable.auto.commit": "true"}
kinp = kop.input(
    "kafka-in", 
    flow, 
    brokers=brokers, 
    topics=["rides"],
    add_config = add_config,
    starting_offset=OFFSET_STORED,
)

event_parsed = op.map("parse_json", kinp.oks, parse_json)

event_filtered = op.filter("filter_null_price", event_parsed, filter_null_price)

event_transformed = op.map("miles2km", event_filtered, miles2km)
event_transformed = op.map("usd2brl", event_transformed, usd2brl)
event_transformed = op.map("add_processing_time", event_transformed, add_processing_time)
event_transformed = op.map("check_dynamic_fare", event_transformed, check_dynamic_fare)
_ = op.map("show_record", event_transformed, show_record) # TODO: this is just for debugging purposes

event_serialized = op.map("serialize_json", event_transformed, serialize_json)

# Define the Kafka output
event_processed = op.map("map_to_kafka_message", event_serialized, lambda x: KafkaSinkMessage(None, x))
kop.output("kafka-out", event_processed, brokers=brokers, topic="rides-refined")

print('Dataflow running..')