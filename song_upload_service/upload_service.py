from flask import Flask, render_template, request
import pika

import base64
import json
app = Flask(__name__)

RABBITMQ_IP = ""
RABBITMQ_PASS = "a_simple_user"
RABBITMQ_USER = "a_simple_user"


@app.route('/', methods=['GET', 'POST'])
def index():



    if request.method == 'POST':
        f = request.files['file']
        file_as_bytes = f.read()

        binary_part= base64.b64encode(file_as_bytes)
        json_to_send = json.dumps(binary_part.decode())

        parameters = pika.URLParameters(f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_IP}:5672/%2f')
        pika_connection = pika.BlockingConnection(parameters)
        channel = pika_connection.channel()
        exchange_name = 'song_transformation_exchange'
        queue_name = 'song_transformation_queue'


        channel.basic_publish(exchange=exchange_name, routing_key=queue_name,
                                        body=json_to_send,
                                        properties=pika.BasicProperties(delivery_mode=2))

        # save file
        #f.save(f.filename)
        return render_template('index.html', message='File Uploaded Successfully')
    return render_template('index.html')





if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=6050,threaded=True)
