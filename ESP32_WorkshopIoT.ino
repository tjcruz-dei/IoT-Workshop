#include <WiFi.h>
#include <PubSubClient.h>
#include <esp_wifi.h>

#define ChanID "01A";

// Set your new MAC Address
uint8_t newMACAddress[] = {0xF2, 0x5E, 0xA4, 0x00, 0x00, 0x00};

//Topics
const char rcvTopic[]="/commands/" ChanID;

// Replace the next variables with your SSID/Password combination
const char* ssid = "SSID";
const char* password = "pass";

// Add your MQTT Broker IP address, example:
const char* mqtt_server = "10.254.0.250";

const char* mqttUser = "user";
const char* mqttPassword = "password";

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  WiFi.disconnect();
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  pinMode(15,OUTPUT);
}

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  //esp_wifi_set_mac(WIFI_IF_STA, &newMACAddress[0]);
  Serial.println(WiFi.macAddress());

  WiFi.setHostname("ESP32SA");
  WiFi.begin(ssid, password);
  
  int c=1;
  while (WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
    if (c>40) {
      //Stupid workaround to deal with the Dept. DHCP server
      WiFi.disconnect();
      newMACAddress[2]=(uint8_t) random(255);
      newMACAddress[3]=(uint8_t) random(255);
      newMACAddress[4]=(uint8_t) random(255);
      newMACAddress[5]=(uint8_t) random(255);
      esp_wifi_set_mac(WIFI_IF_STA, &newMACAddress[0]);
      Serial.println(WiFi.macAddress());
      c=0;
    }
    if (c==0) WiFi.begin(ssid, password);
    c++;
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  
}

void callback(char* topic, byte* message, unsigned int length) {  
    char* buff=(char *) malloc(length+1);
    strncpy(buff,(char *) message,length);
 
    Serial.println(buff);
    digitalWrite(15,(strcmp(buff,"ON"))==0);
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP32ClientXPTO", mqttUser, mqttPassword )) {
      Serial.println("connected");
      // Subscribe
      client.subscribe(rcvTopic);;
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }

  client.loop();

  int LDR = analogRead(35);  
  char TXbuf[5]="";
  sprintf(TXbuf, "%d", LDR);
  
  client.publish("/robot/D1", TXbuf);
  delay(500); 
}
