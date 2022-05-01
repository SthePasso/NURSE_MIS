# python 3.6
# https://www.emqx.com/en/blog/how-to-use-mqtt-in-python

import random
import time
#####
from nurse_mis import NurseMis, ObservationSpace, Smart

from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'emqx'
password = 'public'
AnaNeri = NurseMis("Ana Neri", "Hi I am NURSE MIS!") # the first nurse in Brasil (1814)
Brain = Smart("tflite_models/model_conv2d.tflite")
House = ObservationSpace("House")
    

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    client.AnaNeri = AnaNeri
    client.House = House
    client.Brain = Brain
    return client


def publish(client):
    msg_count = 0
    while True:
        time.sleep(1)
        AnaNeri.talk()
        position = AnaNeri.movePublisher(House)

        image = "tflite_models/george.png"

        #tflite_model_predictions = Brain.interface(image) #how can I receive the image with protocols
        img = [[0,0],[1,1]]
        #print(Brain.modelImg(img))
        #plot_result(tflite_model_predictions, image)

        msg = position #f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
