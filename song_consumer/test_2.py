from io import BytesIO
from flask import Flask, Response
import pika
import json
import os
import rabbitpy

import time

import base64
import requests



RABBITMQ_IP = ""
RABBITMQ_PASS = "a_simple_user"
RABBITMQ_USER = "a_simple_user"



parameters = pika.URLParameters(f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_IP}:5672/%2f')
pika_connection = pika.BlockingConnection(parameters)
channel = pika_connection.channel()

exchange_name = 'song_exchange'
queue_name = 'song_queue'


_,_,body = channel.basic_get(queue=queue_name,auto_ack=True)
message_json = json.loads(body.decode())
decode_string = base64.b64decode(message_json)
print(type(decode_string))

file_like = BytesIO(decode_string)
print(type(file_like))
