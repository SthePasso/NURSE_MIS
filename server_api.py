# python 3.6
# https://www.emqx.com/en/blog/how-to-use-mqtt-in-python

import random
import time
#####
#from nurse_mis import NurseMis, ObservationSpace
from Smart import Smart
from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'emqx'
password = 'public'
#AnaNeri = NurseMis("Ana Neri", "Hi I am NURSE MIS!") # the first nurse in Brasil (1814)
Brain = Smart("tflite_models/model_conv2d.tflite", "tf_models/model_conv2D.h5")
#House = ObservationSpace("House")
    
imageTopic = "Bb4Qimages"
orderTopic = "abc123sendAOrder"

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
    #client.AnaNeri = AnaNeri
    #client.House = House
    client.Brain = Brain
    return client



def on_message(client, userdata, msg):
        time.sleep(5)
        #print(f"Image `{msg.payload.decode()}` from `{msg.topic}` topic")
        print(f"Image from camera send to `{msg.topic}` topic")
        position = 7
        image = Brain.getImageJson(msg.payload)
        #id = Brain.interfaceClassification(image)
        id = Brain.interfaceTF(image)
        print("Id: ", id)
        client.publish(orderTopic, id)
        time.sleep(5)

        #AnaNeri.moveSubscribe(position, House)


def run():
    client = connect_mqtt()
    result = client.publish(orderTopic, "hello")
    print(result)
    client.subscribe(imageTopic)
    client.on_message = on_message
    client.loop_forever()
    


if __name__ == '__main__':
    run()
