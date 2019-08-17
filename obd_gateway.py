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

def payload2json(payload):
    return json.dumps(payload)

def newval(r):
    try:
        payload = {'value': '{0.magnitude}'.format(r.value), 'name': r.command.name, 'time': r.time, 'units': '{0.units}'.format(r.value) }

        payload = { **payload, **pids[r.command.name] }

        topic = '/obd/{0}'.format(r.command.name)

        client.reconnect()
        client.publish(topic, payload2json(payload))

    except:
        logging.exception('MQTT publish failed')

def main(port):
    connection = obd.Async(port)

    for pid in pids:
	    connection.watch(obd.commands[pid], callback=newval) # keep track of the RPM

    connection.start() # start the async update loop

    while True:
        time.sleep(2)

        topic = '/obd_status/connection'
        payload = {'status': connection.status(), 'protocol_name': connection.protocol_name()}

        logging.info(topic, payload)

        client.reconnect()
        client.publish(topic, payload2json(payload))

        logging.info(topic, payload)
        topic = '/obd_status/pids'
        payload = list(pids.keys())

        client.reconnect()
        client.publish(topic, payload2json(payload))


if __name__ == '__main__':
    port = os.getenv('OBDPORT', '/dev/ttyUSB0')
    logging.warning(f'Using OBD port {port}')

    client.connect('localhost', 1883, 60, bind_address="")

    main(port)
