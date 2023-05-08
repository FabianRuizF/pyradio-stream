import pika
import json
import os
import rabbitpy

import time


RABBITMQ_IP = ""
RABBITMQ_PASS = "a_simple_user"
RABBITMQ_USER = "a_simple_user"

parameters = pika.URLParameters(f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_IP}:5672/%2f')
pika_connection = pika.BlockingConnection(parameters)
channel = pika_connection.channel()

exchange_name = 'song_exchange'
#channel.exchange_declare(exchange=exchange_name, exchange_type='direct',durable=True)

queue_parameters = channel.queue_declare(queue='') #,exclusive=True)
queue_name = queue_parameters.method.queue
print(queue_name)
channel.queue_bind(exchange=exchange_name, queue=queue_name)
