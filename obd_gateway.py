#!/usr/bin/python3
import time
import json
import logging
import os

import obd
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

from pids import *

client = mqtt.Client()

def newval(r):
    try:
        payload_dict = {'value': '{0.magnitude}'.format(r.value), 'name': r.command.name, 'time': r.time, 'units': '{0.units}'.format(r.value) }

        payload = json.dumps(payload_dict)
        topic = '/obd/{0}'.format(r.command.name)

        client.reconnect()
        client.publish(topic, payload)

    except:
        logging.exception('MQTT publish failed')

def main(port):
    connection = obd.Async('/dev/pts/0')

    for pid in pids:
	    connection.watch(obd.commands[pid], callback=newval) # keep track of the RPM

    connection.start() # start the async update loop

    while True:
	    time.sleep(1)


if __name__ == '__main__':
    port = os.getenv('OBDPORT', '/dev/ttyUSB0')
    logging.warning(f'Using OBD port {port}')

    client.connect('localhost', 1883, 60)

    main(port)