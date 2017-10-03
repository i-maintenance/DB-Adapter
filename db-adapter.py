import os
import sys
import time
import json
import logging

from logstash import TCPLogstashHandler
# from kafka import KafkaConsumer
# sudo apt-get install librdkafka-dev python-dev
# pip3 install confluent-kafka
from confluent_kafka import Consumer, KafkaError

__date__ = "20 Juli 2017"
__email__ = "christoph.schranz@salzburgresearch.at"
__status__ = "Development"
# 2 Sending multiple topics

KAFKA_TOPICS = ["PrinterData", "SensorData"]
bootstrap_servers = 'il061,il062,il063'
group_id = "db-adapter"
host = 'il063'

def build_pipe():
    logging.basicConfig(level='WARNING')

    # setup logging
    logger = logging.getLogger(str(KAFKA_TOPICS))
    logger.setLevel(logging.INFO)
    logstash_handler = TCPLogstashHandler(host=os.getenv('LOGSTASH_HOST', host),
                                          port=int(os.getenv('LOGSTASH_PORT', 5000)),
                                          version=1)
    logger.addHandler(logstash_handler)

    consumer = Consumer({'bootstrap.servers': bootstrap_servers, 'group.id': 'group_id',
                         'default.topic.config': {'auto.offset.reset': 'smallest'}})
    consumer.subscribe(KAFKA_TOPICS)
    logger.info('Checking topics: {}'.format(str(KAFKA_TOPICS)))

    running = True
    while running:
        msg = consumer.poll()
        if not msg.error():
            data = json.loads(msg.value().decode('utf-8'))
            print(data)
            logger.info('', extra=data)
        elif msg.error().code() != KafkaError._PARTITION_EOF:
            print(msg.error())
            running = False

    consumer.close()


if __name__ == '__main__':
    build_pipe()
