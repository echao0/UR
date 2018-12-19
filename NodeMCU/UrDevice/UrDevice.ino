/*
    This sketch sends a string to a TCP server, and prints a one-line response.
    You must run a TCP server in your local network.
    For example, on Linux you can use this command: nc -v -l 3000
*/

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>


#ifndef STASSID
#define STASSID "Teresawifi"
#define STAPSK  "locastela"
#endif

int user_passw = 8613;

const char* ssid     = STASSID;
const char* password = STAPSK;

const char* host = "echao.asuscomm.com";
const uint16_t port = 8000;

ESP8266WiFiMulti WiFiMulti;

//----------DEF I/O-------
  int tempPin= A0;
  char out1 = D1;
  char out2 = D2;
  char out3 = D3;
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
        delay(500);
        client.println("name,UrNode");
      }
 //----------------------------------------
 
    while (client.connected()) {
         
     /*   if (digitalRead(0) == 0){
          client.println("TestNodeMcu");
          Serial.println("Test send");
          }
       */  
        Serial.println("receiving from remote server");
        String line = client.readStringUntil('\r');
        Serial.println(line);
            
          if (line == "alive"){
                client.println("alive,UrNode");
            }
            
           if (line == "DeviceOn"){
                Serial.println ("Enciendo todo");
                client.println("Enciendo todo");
                digitalWrite(out1, alto);
            }
            
           if (line == "DeviceOff"){
                Serial.println ("Apago todo");
                client.println("Apago todo");
                digitalWrite(out1, bajo);
              }
          
        delay(100);
   }
   
  Serial.println("closing connection");
  client.stop();

  Serial.println("wait 5 sec... to reconnect");
  delay(5000);
}
