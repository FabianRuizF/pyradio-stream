import numpy as np
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

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


filepath = "/root/pyradio-stream/song_producer/tmp.wav"
with open(filepath, 'rb') as f:
#    audio_encoded = base64.b64encode(f.read())
    audio_encoded = f.read()
parameters = pika.URLParameters(f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_IP}:5672/%2f')
pika_connection = pika.BlockingConnection(parameters)
channel = pika_connection.channel()

exchange_name = 'song_exchange'
queue_name = 'song_queue'

import struct


for a in range(300):
    part = audio_encoded[44100*2*(a):44100*2*(a+1)]
    binary_part= base64.b64encode(part)
    channel.basic_publish(exchange_name,queue_name
                                    json.dumps(binary_part.decode()),
                                    pika.BasicProperties(delivery_mode=2))


#channel.basic_publish(exchange_name,queue_name,
#                                json.dumps(audio_encoded.decode()),
#                                pika.BasicProperties(delivery_mode=2))
