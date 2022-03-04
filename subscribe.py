# python3.6
# https://www.emqx.com/en/blog/how-to-use-mqtt-in-python

import random
import time
###
from nurse_mis import NurseMis, ObservationSpace

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
House = ObservationSpace("House")

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

    return client


def subscribe(client: mqtt_client):

    def on_message(client, userdata, msg):
        print(f"Here is `{msg.payload.decode()}` from `{msg.topic}` topic")
        time.sleep(1)
        position = 7
        position = msg.payload.decode()[0]
        #print(position,"\n\n\n\n")
        AnaNeri.moveSubscribe(position, House)
        
    client.subscribe(topic)
    client.subscribe(position)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
