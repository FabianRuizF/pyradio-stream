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


@app.route("/wav")
def streamwav():
    def generate():
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
        data_audio = BytesIO(decode_string)
        data = data_audio.read(1024)
        while data:
            yield data
            data = data_audio.read(1024)
    return Response(generate(), mimetype="audio/x-wav")



if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
