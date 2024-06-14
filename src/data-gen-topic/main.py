import sys
import time
import json
import random
import pandas as pd
from kafka import KafkaProducer
from dotenv import load_dotenv

from api import api_requests
from objects import users as users_obj, rides as rides_obj
from config import URLS

params = {'size': 10}
users = users_obj.Users()
rides = rides_obj.Rides()
api = api_requests.Requests()

class TopicWriter:
    """
    This class is used to write events into a kafka topic
    """

    def __init__(self, 
        topic_name=None, 
        broker='localhost:9092'
    ):
        """
        Initialize the class with the provided parameters.

        :param topic_name: The name of the topic to write into.
        :type broker: str

        :param broker: the broker server url.
        :type access_key: str 
        """

        self.topic_name = topic_name
        self.broker = broker

        # Initialize the Kafka producer
        if topic_name:
            self.producer = KafkaProducer(
                bootstrap_servers=broker,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
    

    def _create_dataframe(self, dt, is_cpf=None):
        pd_df = pd.DataFrame(dt)
        # print(pd_df.info())
        pd_df['user_id'] = api.gen_user_id(params['size'])
        pd_df['dt_current_timestamp'] = api.gen_timestamp()
        if is_cpf:
            pd_df['cpf'] = [api.gen_cpf() for _ in range(len(pd_df))]

        return json.loads(pd_df.to_json(orient="records").encode('utf-8') )


    def unit_produce(self, save=True):

        gen_cpf = api.gen_cpf()

        dt_riders = rides.get_multiple_rows(gen_dt_rows=params['size'])
        
        dt_riders =  self._create_dataframe(dt_riders, is_cpf=True)


        if save:
            for record in dt_riders:
                self.producer.send(self.topic_name, record)
                self.producer.flush()
                
                print(f"Message sent: {record}")
        
        else:
            print(dt_riders[0])
        



if __name__ == '__main__':
    args = sys.argv
    kp = TopicWriter(args[1])

    kp.unit_produce()
