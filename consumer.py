import json

from kafka import KafkaConsumer, KafkaProducer


def last_full_minute(timestamp: int):
    """Calculates the last full minute of a given timestamp in milliseconds, for example given the timestamp
    equivalent of Saturday, 13 August 2022 14:45:37.567 the function returns the timestamp equivalent of
    Saturday, 13 August 2022 14:45:00.000.
    """
    return timestamp - (timestamp % 60000)


if __name__ == '__main__':
    server = 'localhost:9092'
    topic = 'wiki-edits'

    consumer = KafkaConsumer(topic, bootstrap_servers=server, auto_offset_reset='earliest',
                             # a consumer needs to be part of a consumer group to make the auto commit work
                             # https://towardsdatascience.com/kafka-python-explained-in-10-lines-of-code-800e3e07dad1
                             enable_auto_commit=True, group_id='edits-per-minute',
                             value_deserializer=lambda v: json.loads(v.decode('utf-8')))

    producer = KafkaProducer(bootstrap_servers=server, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    current_lfm = 0
    edit_count_global = 0
    edit_count_de = 0

    for message in consumer:
        lfm = last_full_minute(message.timestamp)

        if lfm >= current_lfm + 60000:
            # send edit counts to Kafka topics if next full minute has begun
            if current_lfm:  # skip initial count for timestamp 0
                producer.send('edits-per-minute-global', {
                    'timestamp': current_lfm,
                    'edits': edit_count_global
                })
                producer.send('edits-per-minute-de', {
                    'timestamp': current_lfm,
                    'edits': edit_count_de
                })
                print(f'{edit_count_global} global and {edit_count_de} german edits per minute at {current_lfm}')

            # reset counters and update lfm
            edit_count_global = 0
            edit_count_de = 0
            current_lfm = lfm

        edit_count_global += 1
        if message.value['wiki'] == 'dewiki':
            edit_count_de += 1
