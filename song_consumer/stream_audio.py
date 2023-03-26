import time
from flask import Flask, render_template, Response
from io import BytesIO

from flask import Flask, Response
import pika
import json
import os
import rabbitpy

import time

import base64
import requests

app = Flask(__name__)

def genHeader(sampleRate, bitsPerSample, channels):
    datasize = 2000*10**6
    o = bytes("RIFF",'ascii')                                               # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(4,'little')                               # (4byte) File size in bytes excluding this and RIFF marker
    o += bytes("WAVE",'ascii')                                              # (4byte) File type
    o += bytes("fmt ",'ascii')                                              # (4byte) Format Chunk Marker
    o += (16).to_bytes(4,'little')                                          # (4byte) Length of above format data
    o += (1).to_bytes(2,'little')                                           # (2byte) Format type (1 - PCM)
    o += (channels).to_bytes(2,'little')                                    # (2byte)
    o += (sampleRate).to_bytes(4,'little')                                  # (4byte)
    o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4,'little')  # (4byte)
    o += (channels * bitsPerSample // 8).to_bytes(2,'little')               # (2byte)
    o += (bitsPerSample).to_bytes(2,'little')                               # (2byte)
    o += bytes("data",'ascii')                                              # (4byte) Data Chunk Marker
    o += (datasize).to_bytes(4,'little')                                    # (4byte) Data size in bytes
    return o




@app.route('/audio')
def audio():
    # start Recording
    def sound():

        #wav_header = genHeader(sampleRate, bitsPerSample, channels)


        RABBITMQ_IP = ""
        RABBITMQ_PASS = "a_simple_user"
        RABBITMQ_USER = "a_simple_user"



        parameters = pika.URLParameters(f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_IP}:5672/%2f')
        pika_connection = pika.BlockingConnection(parameters)
        channel = pika_connection.channel()


        exchange_name = 'song_exchange'


        queue_parameters = channel.queue_declare(queue='',exclusive=True)
        queue_name = queue_parameters.method.queue
        channel.queue_bind(exchange=exchange_name, queue=queue_name)

        _,_,body = channel.basic_get(queue=queue_name,auto_ack=True)
        while(body is None):
            print("waiting")
            time.sleep(1)
            _,_,body = channel.basic_get(queue=queue_name,auto_ack=True)
        message_json = json.loads(body.decode())
        decode_string = base64.b64decode(message_json)
        print(type(decode_string))
        data_audio = BytesIO(decode_string)


        CHUNK = 1024
#        sampleRate = 44100
#        bitsPerSample = 16
#        channels = 1


        sampleRate = 44100
        bitsPerSample = 16
        channels = 1

        wav_header = genHeader(sampleRate, bitsPerSample, channels)
        #data = data_audio.read(1024)


        first_run = True
        while True:
           if first_run:
               data = wav_header + data_audio.read(CHUNK)
               first_run = False
           else:
               data = data_audio.read(1024)
           print(len(data))
           if(len(data)==0):
               _,_,body = channel.basic_get(queue=queue_name,auto_ack=True)
               while(body is None):
                   print("waiting")
                   time.sleep(1)
                   _,_,body = channel.basic_get(queue=queue_name,auto_ack=True)
               message_json = json.loads(body.decode())
               decode_string = base64.b64decode(message_json)
               print(type(decode_string))
               data_audio = BytesIO(decode_string)
               data = data_audio.read(1024)
           yield(data)
    return Response(sound())


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('./index.html')


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",threaded=True)
