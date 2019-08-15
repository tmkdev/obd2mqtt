#!/usr/bin/python3
import time
import json

import obd
import paho.mqtt.publish as publish

from pids import *

def newval(r):
	try:
		payload_dict = {'value': '{0.magnitude}'.format(r.value), 'name': r.command.name, 'time': r.time, 'units': '{0.units}'.format(r.value) }

		payload = json.dumps(payload_dict)
		topic = '/obd/{0}'.format(r.command.name)

		publish.single(topic, payload, hostname="localhost")
	except:
		print("Broken..")


connection = obd.Async('/dev/pts/0')

for pid in pids:
	connection.watch(obd.commands[pid], callback=newval) # keep track of the RPM

connection.start() # start the async update loop

while True:
	time.sleep(0.1)
