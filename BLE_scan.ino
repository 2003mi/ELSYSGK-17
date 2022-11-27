// Import required libraries
#include "WiFi.h"
#include "ESPAsyncWebServer.h"

// Set your access point network credentials
const char* ssid = "ESP32-Access-Point";
const char* password = "123456789";

/*#include <SPI.h>
#define BME_SCK 18
#define BME_MISO 19
#define BME_MOSI 23
#define BME_CS 5*/


// Create AsyncWebServer object on port 80
AsyncWebServer server(80);

const int buttonPin = 15;
int buttonState = 0;
int pinActive = 0;
String val = "False";

void setup(){
  pinMode(buttonPin, INPUT);
  // Serial port for debugging purposes
  Serial.begin(115200);
  Serial.println();
  
  // Setting the ESP as an access point
  Serial.print("Setting AP (Access Point)…");
  // Remove the password parameter, if you want the AP (Access Point) to be open
  WiFi.softAP(ssid, password);

  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(IP);
  Serial.println(val);
  server.on("/signal", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/plain", val.c_str());
  });
  
  bool status;
  
  // Start server
  server.begin();
}
void loop()
{
  buttonState = digitalRead(buttonPin);
  delay(10);
  if (pinActive == 0 && buttonState == HIGH)
  {
    pinActive = 1;
    if(val == "False"){
      val = "True";
      }
     else {
      val = "False";
      }
    Serial.println(val);
  }
  else if (pinActive == 1 && buttonState == LOW)
  {
    pinActive = 0;
  }
  // check if the pushbutton is pressed.
  // if it is, the buttonState is HIGH
} 
