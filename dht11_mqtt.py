#!/usr/bin/python
import paho.mqtt.client as mqtt
import time
import sys
import Adafruit_DHT

time.sleep(5) #Sleep to allow wireless to connect before starting MQTT

#These are the credentials and connection commands for Cayenne IoT platform
# Not used at this point
"""
username = "MQTT Username From Dashboard"
password = "MQTT Passsword From Dashboard"
clientid = "MQTT Client ID From Dashboard"
mqttc.username_pw_set(username, password=password)
mqttc.connect("mqtt.mydevices.com", port=1883, keepalive=60)
"""
username = "pi" # While noty using Cayenne credentials
#password = "raspberry"
clientid = "101" 

# Start mqtt client
mqttc = mqtt.Client(client_id=clientid)
mqttc.loop_start()

# Create the route for the topics

topic_dht11_temp = "v1/" + username + "/things/" + clientid + "/data/1"
topic_dht11_humidity = "v1/" + username + "/things/" + clientid + "/data/2"
# Not using DHT22 sensor now
#topic_dht22_temp = "v1/" + username + "/things/" + clientid + "/data/3"
#topic_dht22_humidity = "v1/" + username + "/things/" + clientid + "/data/4"

while True:
    try:
        humidity11, temp11 = Adafruit_DHT.read_retry(11, 2) #11 is the sensor type, 2 is the GPIO pin number (not physical pin number)
#        humidity22, temp22 = Adafruit_DHT.read_retry(22, 18) #22 is the sensor type, 18 is the GPIO pin number (not physical pin number)
        
        if temp11 is not None:
            temp11 = "temp,c=" + str(temp11)
            mqttc.publish(topic_dht11_temp, payload=temp11, retain=True)
        if humidity11 is not None:
            humidity11 = "rel_hum,p=" + str(humidity11)
            mqttc.publish(topic_dht11_humidity, payload=humidity11, retain=True)
        """
        if temp22 is not None:
            temp22 = "temp,c=" + str(temp22)
            mqttc.publish(topic_dht22_temp, payload=temp22, retain=True)
        if humidity22 is not None:
            humidity22 = "rel_hum,p=" + str(humidity22)
            mqttc.publish(topic_dht22_humidity, payload=humidity22, retain=True)
        """
        time.sleep(5)
    except (EOFError, SystemExit, KeyboardInterrupt):
        mqttc.disconnect()
        sys.exit()