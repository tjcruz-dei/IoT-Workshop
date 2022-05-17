import ssl
import os
import socket
import time,random
from paho.mqtt import client as mqtt_client

broker=''
port = 1883

topicSuffix="01A"
topic_send = "/command/"+topicSuffix
topic_recv = "/status/"+topicSuffix

username = ''
password = ''

#MQTT Connect
def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            subscribe(client)
        else:
            print("Failed to connect, return code "+str(rc))

    def on_disconnect(client, userdata, rc):
        if rc != 0:
           print("Unexpected disconnection.")

    client_id = f'htb--mqtt-{random.randint(0, 100)}-'+str(time.time())
    client = mqtt_client.Client(client_id+str(os.getpid())+str(time.time()))
    client.username_pw_set(username,password)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    
    #client.tls_set(cert_reqs=ssl.CERT_NONE)
    #client.tls_insecure_set(True)

    client.connect(broker, port)

    #If latency is a concern
    client.socket().setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
    return client

#MQTT Subscribe
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        message=msg.payload.decode().rstrip()
        print(f"Received `{message}` from `{msg.topic}` topic")

    client.subscribe(topic_recv,qos=0)
    client.on_message = on_message
    #print("SUB:"+topic_recv+" PUB:"+topic_send)

#MQTT Pub
def publish(client,msg,topic_send):
    result = client.publish(topic_send, msg,qos=0)
    # result: [0, 1]
    status = result[0]
    if (status!=0):
        print(f"Failed to send message to topic {topic_send}")

#Initialization
if __name__ == "__main__":	
	client=connect_mqtt()
	client.loop_start()

	time.sleep(0.5)	
	command=""
	while (command!="STOP"):
		command=input("\n"+"command:")
		publish(client,command,topic_send)
	client.disconnect()
