#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json

import paho
import paho.mqtt.client as mqtt
from guage import Guage
from pids import *

g = Guage()

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))

def on_message(mqttc, obj, msg):
    pdict = json.loads(msg.payload)
    g.display(pdict)

def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)

mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

mqttc.connect("localhost", 1883, 60)
mqttc.subscribe("/obd/SPEED", 0)

mqttc.loop_forever()
