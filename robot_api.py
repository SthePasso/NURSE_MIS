# python3.6
# https://www.emqx.com/en/blog/how-to-use-mqtt-in-python

from email.mime import image
import random
import time
from Smart import Smart

###
from NurseMis import NurseMis, ObservationSpace

from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
position = "w"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'emqx'
password = 'public'
AnaNeri = NurseMis("Ana Neri", "Hi I am NURSE MIS!") # the first nurse in Brasil (1814)
Brain = Smart("tflite_models/model_conv2d.tflite")
House = ObservationSpace("House")

imageTopic = "Bb4Qimages"
orderTopic = "abc123sendAOrder"


def connect_mqtt() -> mqtt_client:
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


def subscribe(client: mqtt_client):

    def on_message(client, userdata, msg):
        print(f"Here is `{msg.payload.decode()}` from `{msg.topic}` topic")
        time.sleep(1)
        position = 7
        position = msg.payload.decode()[0]
        #AnaNeri.moveSubscribe(position, House)

        
    client.subscribe(orderTopic)
    #client.subscribe(position)
    client.on_message = on_message

def publish(client):
    msg_count = 0
    time.sleep(1)
    AnaNeri.talk()
    position = AnaNeri.getImage()#movePublisher(House)
    #image = AnaNeri.image()
        #tflite_model_predictions = Brain.interface(image) #how can I receive the image with protocols
        #print(Brain.modelImg(img))
        #plot_result(tflite_model_predictions, image)

    msg = position
    #msg = image
    result = client.publish(imageTopic, msg)
    status = result[0]
    if status == 0:
        print(f"Send to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")
        #print(result)
    msg_count += 1

def run():
    client = connect_mqtt()
    subscribe(client)
    while True:
        client.loop()
        image = AnaNeri.getImage()
        publish(client)
        # Got message, do work
        # done with work, continue


if __name__ == '__main__':
    run()
