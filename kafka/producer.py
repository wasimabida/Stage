from kafka import KafkaProducer
from dotenv import load_dotenv
import os

load_dotenv()

def send_to_kafka(data, topic_name='topic_name'):
    kafka_server = os.getenv("KAFKA_SERVER")
    kafka_port = os.getenv("KAFKA_PORT")
    
    producer = KafkaProducer(bootstrap_servers=f"{kafka_server}:{kafka_port}")
    
    for item in data:
        producer.send(topic_name, value=item.encode('utf-8'))
    
    producer.close()

