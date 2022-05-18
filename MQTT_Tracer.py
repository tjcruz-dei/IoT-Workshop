import ssl
import os
import socket
import time,random
from paho.mqtt import client as mqtt_client
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

broker=''
port = 1883

topicSuffix="01A"
topic_send = "/command/"+topicSuffix
topic_recv = "/status/"+topicSuffix

username = ''
password = ''

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):
    # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('LDR Measurement')
    plt.ylabel('ADC Scale')

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

        val_LDR = int(message)
        xs.append(time.time())
        ys.append(val_LDR)

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

	# Set up plot to call animate() function periodically
	ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=200)
	plt.show()



