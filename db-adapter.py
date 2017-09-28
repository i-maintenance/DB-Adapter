import os
import sys
import time
import json
import logging

from logstash import TCPLogstashHandler
from kafka import KafkaConsumer
import concurrent.futures

__date__ = "20 Juli 2017"
__email__ = "christoph.schranz@salzburgresearch.at"
__status__ = "Development"
# 2 Sending multiple topics

KAFKA_TOPICS = ["PrinterData", "SensorData"]
HOST = 'il063'


def distribute_tasks():
    logging.basicConfig(level='WARNING')

    pool = concurrent.futures.ThreadPoolExecutor(max_workers=10)
    pool.map(send_to_logstash, KAFKA_TOPICS)

def send_to_logstash(topic):
    # setup logging
    logger = logging.getLogger(topic)
    logger.setLevel(logging.INFO)
    logstash_handler = TCPLogstashHandler(host=os.getenv('LOGSTASH_HOST', HOST),
                                          port=int(os.getenv('LOGSTASH_PORT', 5000)),
                                          version=1)
    logger.addHandler(logstash_handler)

    consumer = KafkaConsumer(
            bootstrap_servers=['il061', 'il062', 'il063'],
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            api_version=(0, 9))
    consumer.subscribe([topic])
    logger.info('Checking topics %s', consumer.subscription())

    for msg in consumer:
        logger.info(topic, extra=msg.value)


if __name__ == '__main__':
    distribute_tasks()