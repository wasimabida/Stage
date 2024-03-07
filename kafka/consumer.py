from kafka import KafkaConsumer
import csv
from dotenv import load_dotenv
import os

load_dotenv()

def consume_from_kafka_and_save_to_csv(filename='posts.csv', topic_name='topic_name'):
    kafka_server = os.getenv("KAFKA_SERVER")
    kafka_port = os.getenv("KAFKA_PORT")
    
    consumer = KafkaConsumer(topic_name, bootstrap_servers=f"{kafka_server}:{kafka_port}")
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        for message in consumer:
            text = message.value.decode('utf-8')
            writer.writerow([text])
    
    consumer.close()
