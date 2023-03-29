
import numpy as np
import pika
import json
import os
import rabbitpy

import time

import pyaudio
import wave



RABBITMQ_IP = ""
RABBITMQ_PASS = "a_simple_user"
RABBITMQ_USER = "a_simple_user"

import base64
import requests

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

#change to get audio from flask service
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


wf = wave.open(filepath, 'rb') 
p = pyaudio.PyAudio()
bit_len = p.get_format_from_width(wf.getsampwidth())
channels = wf.getnchannels()
rate = int(wf.getframerate())

json_to_send = {}
json_to_send["bit_len"] = bit_len
json_to_send["channels"] =channels
json_to_send["rate"] =rate
print(len(audio_encoded)/rate/2)
exit()
for a in range(30):
    #psuedo code, change to get the final inde
    if(a=="finish encode"):
        part = audio_encoded[rate*2*(a):]
    else:
        part = audio_encoded[rate*2*(a):rate*2*(a+1)]
    binary_part= base64.b64encode(part)
    json_to_send["data"] = binary_part.decode()
    channel.basic_publish(exchange=exchange_name, routing_key="",
                                    body=json.dumps(json_to_send),
                                    properties=pika.BasicProperties(delivery_mode=2))
    time.sleep(0.9)

#channel.basic_publish(exchange_name,queue_name,
#                                json.dumps(audio_encoded.decode()),
#                                pika.BasicProperties(delivery_mode=2))
