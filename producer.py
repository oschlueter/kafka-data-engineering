import csv
import json
import logging
import random
import time

from kafka import KafkaProducer

if __name__ == '__main__':
    server = 'localhost:9092'
    topic = 'wiki-edits'

    producer = KafkaProducer(bootstrap_servers=server, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    with open('data/sample_data.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file)

        for event in reader:
            # configured Kafka auto.create.topics.enable to automatically generate topics
            producer.send('wiki-edits', event)
            logging.debug(f'sent {event}')

            # emit data in random intervals between 0 and 1 seconds to emulate real-world behaviour
            time.sleep(random.uniform(0, 1))
