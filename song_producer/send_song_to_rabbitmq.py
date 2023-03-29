import soundfile as sf
from pydub import AudioSegment
import pyaudio
import base64
import io
import time
import wave
import librosa
import soundfile as sf
import pika
import json
RABBITMQ_IP = ""
RABBITMQ_PASS = "a_simple_user"
RABBITMQ_USER = "a_simple_user"



parameters = pika.URLParameters(f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_IP}:5672/%2f')
pika_connection = pika.BlockingConnection(parameters)
channel = pika_connection.channel()


exchange_name = 'song_exchange_transformation'
queue_name = "song_transformation_queue"

while(True):
    exchange_name = 'song_exchange_transformation'
    queue_name = "song_transformation_queue"
    _,_,body = channel.basic_get(queue=queue_name,auto_ack=True)
    while(body is None):
        print("waiting")
        time.sleep(1)
        _,_,body = channel.basic_get(queue=queue_name,auto_ack=True)


    body = body.decode()
    body = json.loads(body)
    decode_string = base64.b64decode(body)

    with open("temp.audio", 'wb') as f: 
        f.write(decode_string)



    x,_ = librosa.load("temp.audio",sr=22050)
    sf.write('tmp.wav', x, 22050)

    with open('tmp.wav', 'rb') as f:
        audio_encoded = f.read()



    wf = wave.open('tmp.wav', 'rb') 
    p = pyaudio.PyAudio()

    bit_len = wf.getsampwidth() * 8
    channels = wf.getnchannels()
    rate = int(wf.getframerate())

    json_to_send = {}
    json_to_send["bit_len"] = bit_len
    json_to_send["channels"] =channels
    json_to_send["rate"] =rate
    print(len(audio_encoded)/rate/2)

    exchange_name = 'song_exchange'
    queue_name = 'song_queue'

    for a in range(30):
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
