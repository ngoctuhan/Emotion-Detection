#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import time 
import uuid
import json
def on_connect(client, userdata, flags, rc):
  
  print("Connected with result code "+str(rc))
 
# This is the Publisher
client = mqtt.Client()
client.connect("203.162.10.118",5000,60)
client.username_pw_set("admin", "password")
client.on_connect = on_connect
client.loop_start()
while True:
    print(client.is_connected())
    time.sleep(1)
    if client.is_connected():
       break 
print(client.is_connected())
i = 0
payload = {
      "command": "START",
      "session": "12abc"
}
print(client.publish(f"server/command", json.dumps(payload)))
print('Done')
client.loop_stop()