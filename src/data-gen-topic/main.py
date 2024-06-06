import sys
import time
import json
import random
import pandas as pd
from kafka import KafkaProducer


from api import api_requests
from objects import users as users_obj, rides as rides_obj
from config import URLS


params = {'size': 1000}
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
        self.producer = KafkaProducer(
            bootstrap_servers=broker,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
    

    def _create_dataframe(self, dt, is_cpf=False):
        pd_df = pd.DataFrame(dt)
        # print(pd_df.info())
        pd_df['user_id'] = api.gen_user_id(params['size'])
        pd_df['dt_current_timestamp'] = api.gen_timestamp()
        if is_cpf:
            pd_df['cpf'] = [api.gen_cpf() for _ in range(len(pd_df))]
            pd_df['spending'] = [random.randint(1, 100) for i in range(pd_df.shape[0])]

        return json.loads(pd_df.to_json(orient="records").encode('utf-8') )


    def unit_produce(self):

        dt_users = users.get_multiple_rows(gen_dt_rows=params['size'])
        # dt_rides = rides.get_multiple_rows(gen_dt_rows=100)

        dt_users = self._create_dataframe(dt_users, is_cpf=True)
        # dt_rides = self._create_dataframe(dt_rides)


        for user in dt_users:
            self.producer.send(self.topic_name, user)
            self.producer.flush()
            
            print(f"Message sent: {user}")
        # for ride in dt_rides:
        #     self.producer.send(self.topic_name, ride)
        #     self.producer.flush()
            
        #     print(f"Message sent: {ride}")
        



if __name__ == '__main__':
    args = sys.argv
    kp = TopicWriter(args[1])

    kp.unit_produce()
