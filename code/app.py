import pandas as pd
import json
import threading
import uuid

from pathlib import Path
from kafka import KafkaProducer, KafkaConsumer
from time import sleep

PATH = Path('../Data/')
KAFKA_HOST = 'localhost:9092'

# load the data that is captured real time
df_real = pd.read_csv(PATH/'NKE_test.csv')

df_real['json'] = df_real.apply(lambda x: x.to_json(), axis = 1)

# load the json objects
messages = df_real.json.tolist()


def start_producing():
    """Kafka producer
    sends a single row of data to Kafka topic app_messages 
    with key as 'data'
    """
    producer = KafkaProducer(bootstrap_servers=KAFKA_HOST)
    for i in range(200):
        message_id =str(uuid.uuid4())
        message = {'request_id': message_id, 'data':  json.loads(messages[i])} 
        producer.send('app_messages', json.dumps(message).encode('utf-8'))
        producer.flush()
        print("+++ PRODUCER: Sent message with id {}".format(message_id))
        sleep(60)


def start_consuming():
    """Kafka consumer
    reads prediction from app_messages
    with key as 'prediction'
    """
    consumer = KafkaConsumer('app_messages', bootstrap_servers=KAFKA_HOST)

    for msg in consumer:
        message = json.loads(msg.value)
        if 'prediction' in message:
            request_id = message['request_id']
            print("--- CONSUMER: Received prediction {} for request id {}".format(message['prediction'], request_id))

threads = []
pthread = threading.Thread(target=start_producing)
cthread = threading.Thread(target=start_consuming)
threads.append(pthread)
threads.append(cthread)
pthread.start()
cthread.start()