/*
    This sketch sends a string to a TCP server, and prints a one-line response.
    You must run a TCP server in your local network.
    For example, on Linux you can use this command: nc -v -l 3000
*/

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>


#ifndef STASSID
#define STASSID "Me-House"
#define STAPSK  "Et-micasa"
#endif

int user_passw =8613;
String deviceName = "UrNode2";
 
const char* ssid     = STASSID;
const char* password = STAPSK;

const char* host = "echao.asuscomm.com";
const uint16_t port = 8000;

int online = 0;

ESP8266WiFiMulti WiFiMulti;

//----------DEF I/O-------
  int tempPin= A0;
  char out1 = D1;
  char out2 = D2;
  char out3 = D8;
  char out4 = D4;
  char out5 = D5;
  
  char alto = LOW;
  char bajo = HIGH;
    
//-----------------------------


void setup() {
  Serial.begin(115200);
  
//-----------IN/OUT------------
  pinMode(out1, OUTPUT);
  digitalWrite(out1, bajo);
  pinMode(out2, OUTPUT);
  digitalWrite(out2, bajo);
  pinMode(out3, OUTPUT);
  digitalWrite(out3, bajo);
  pinMode(out4, OUTPUT);
  digitalWrite(out4, bajo);
  pinMode(out5, OUTPUT);
  digitalWrite(out5, bajo);
  pinMode(0, INPUT); // Boton de flash
//-----------------------------

  // We start by connecting to a WiFi network
  WiFi.mode(WIFI_STA);
  WiFiMulti.addAP(ssid, password);

  Serial.println();
  Serial.println();
  Serial.print("Wait for WiFi... ");

  while (WiFiMulti.run() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  delay(500);
}

void loop() {
    Serial.print("connecting to ");
    Serial.print(host);
    Serial.print(':');
    Serial.println(port);
  
    WiFiClient client;
  
    if (!client.connect(host, port)) {
        Serial.println("connection failed");
        Serial.println("wait 5 sec...");
        delay(5000);
        return;
    }
//-----------------Send NAME-------------
    if (client.connected()) {
       client.println(user_passw);
        delay(1500);
        client.println("name," + deviceName);
      }
 //----------------------------------------
 
    while (client.connected()) {
         
     /*   if (digitalRead(0) == 0){
          client.println("TestNodeMcu");
          Serial.println("Test send");
          }
       */  
        String line = client.readStringUntil('\r');
        if (line != ""){
        Serial.println(line);
        }
          if (line == "alive"){
                client.println("urSend,server,alive");
            }
            
           if (line == "DeviceOn"){
                Serial.println ("Enciendo todo");
                client.println("urSend,server,allOn");
                digitalWrite(out1, alto);
                digitalWrite(out2, alto);
                digitalWrite(out3, alto);
                digitalWrite(out4, alto);
            }
            
           if (line == "DeviceOff"){
                Serial.println ("Apago todo");
                client.println("urSend,server,allOff");
                digitalWrite(out1, bajo);
                digitalWrite(out2, bajo);
                digitalWrite(out3, bajo);
                digitalWrite(out4, bajo);
              }
           if (line == "Device1On"){
                Serial.println ("Enciendo 1");
                client.println("urSend,server,d1On");
                digitalWrite(out1, alto);
              }
           if (line == "Device2On"){
                Serial.println ("Enciendo 2");
                client.println("urSend,server,d2On");
                digitalWrite(out2, alto);
              }
           if (line == "Device3On"){
                Serial.println ("Enciendo 3");
                client.println("urSend,server,d3On");
                digitalWrite(out3, alto);
              }
           if (line == "Device4On"){
                Serial.println ("Enciendo 4");
                client.println("urSend,server,d4On");
                digitalWrite(out4, alto);
              }
           if (line == "Device1Off"){
                Serial.println ("Apago 1");
                client.println("urSend,server,d1Off");
                digitalWrite(out1, bajo);
              }
           if (line == "Device2Off"){
                Serial.println ("Apago 2");
                client.println("urSend,server,d2Off");
                digitalWrite(out2, bajo);
              }
           if (line == "Device3Off"){
                Serial.println ("Apago 3");
                client.println("urSend,server,d3Off");
                digitalWrite(out3, bajo);
              }
            if (line == "Device4Off"){
                Serial.println ("Apago 4");
                client.println("urSend,server,d4Off");
                digitalWrite(out4, bajo);
              }
            if (line == "nodeStatus"){
                Serial.println("dentro de Status");
                String  outStatus =  String(!digitalRead(out1));
                outStatus += "/";
                outStatus += String(!digitalRead(out2));
                outStatus += "/";
                outStatus += String(!digitalRead(out3));
                outStatus += "/";
                outStatus += String(!digitalRead(out4));
                Serial.println("NodeUr2," + outStatus);
                client.println("urSend,server," + outStatus);
              }
             

          if (online == 100){
            Serial.println("dentro de online");
            client.println("alive,UrDevice");
            
            String line = client.readStringUntil('\r');
              if (line != "ack"){
              Serial.println("closing connection");
              client.stop();
              }
            online = 0;
            }
            
        delay(100);
        online++;
   }
   
  Serial.println("closing connection");
  client.stop();

  Serial.println("wait 5 sec... to reconnect");
  delay(5000);
}
