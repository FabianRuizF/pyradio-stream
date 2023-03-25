
import pika
import json
import os
import rabbitpy

import time


RABBITMQ_IP = ""
RABBITMQ_PASS = "a_simple_user"
RABBITMQ_USER = "a_simple_user"

import base64
import requests


filepath = "/root/pyradio-stream/song_producer/b_slipout.mp3"
with open(filepath, 'rb') as f:
    audio_encoded = base64.b64encode(f.read())

parameters = pika.URLParameters(f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_IP}:5672/%2f')
pika_connection = pika.BlockingConnection(parameters)
channel = pika_connection.channel()

exchange_name = 'song_exchange'
queue_name = 'song_queue'

channel.basic_publish(exchange_name,queue_name,
                                json.dumps(audio_encoded.decode()),
                                pika.BasicProperties(delivery_mode=2))

