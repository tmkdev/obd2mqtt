#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import logging

import paho
import paho.mqtt.client as mqtt
import time
import datetime
import subprocess

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

i2c = busio.I2C(SCL, SDA)
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
disp.fill(0)
disp.show()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))

draw = ImageDraw.Draw(image)

draw.rectangle((0, 0, width, height), outline=0, fill=0)

padding = -2
top = padding
bottom = height-padding
x = 0

font = ImageFont.load_default()

tx=0
rx=0

def on_connect(mqttc, obj, flags, rc):
    logging.warning("rc: " + str(rc))

def on_message(mqttc, obj, msg):
    global rx, tx
    topicparts = msg.topic.split('/')

    if topicparts[4] == 'sent':
        tx = int(float(msg.payload.decode("utf-8")))
    if topicparts[4] == 'received':
        rx = int(float(msg.payload.decode("utf-8")))

    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")

    msgcounts = f'rxpm: {rx} txpm: {tx}'

    logging.info(msgcounts)

    draw.text((x, top+0), "IP: "+IP, font=font, fill=255)
    draw.text((x, top+8), CPU, font=font, fill=255)
    draw.text((x, top+16), msgcounts, font=font, fill=255)

    disp.image(image)
    disp.show()

def on_subscribe(mqttc, obj, mid, granted_qos):
    logging.warning("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mqttc, obj, level, string):
    logging.warning(string)

mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

mqttc.connect('localhost', 1883, 60, bind_address="")
mqttc.subscribe("$SYS/broker/load/messages/+/1min", 0)

mqttc.loop_forever()
