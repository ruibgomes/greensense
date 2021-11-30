// Included Libraries and modules
#include <SPI.h>          // Serial Peripheral Interface
#include <WiFiNINA.h>     // wifi library
#include <Wire.h>         // Analog connections
#include "DHT.h"          // Temp Humd sensor
#include "Arduino.h"
#include "SI114X.h"       // Light Sensor

#include "arduino_secrets.h" // Where you place SSID and password
// ---------- CONFIGURE NETWORK CONNECTION ----------------------
///////please enter your sensitive data in the Secret tab/arduino_secrets.h
char ssid[] = SECRET_SSID;        // your network SSID (name)
char pass[] = SECRET_PASS;    // your network password (use for WPA, or use as key for WEP)
int keyIndex = 0;                 // your network key Index number (needed only for WEP)

int status = WL_IDLE_STATUS;

WiFiServer server(80);

// ---------- CONFIGURE DHT SENSOR PARAMETERS --------------------
#define DHTPIN 2     // what pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302)

DHT dht(DHTPIN, DHTTYPE);

// ---------- CONFIGURE SOIL MOISTURE SENSOR PARAMETERS ----------
int sensorPin = A0;
int SMsensorValue = 0;
float moist_cal = 700;          // value for 100% (in water)

// ---------- CONFIGURE LIGHT SENSOR PARAMETERS ------------------
SI114X SI1145 = SI114X();

// ---------------------------------------------------------------------------------------------------------
// ---------------------------------------------------------------------------------------------------------
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
   
   // Initialize serials (mainly for debugging when connected to USB)
  Serial.begin(9600);
  
  // -------------SETUP FOR NETWORK CONNECTION:----------------------
  // Wait for port to open:
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  // check for the WiFi module:
  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("Communication with WiFi module failed!");
    // don't continue
    while (true);
  }

  String fv = WiFi.firmwareVersion();
  if (fv < WIFI_FIRMWARE_LATEST_VERSION) {
    Serial.println("Please upgrade the firmware");
  }

  // attempt to connect to Wifi network:
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
    status = WiFi.begin(ssid, pass);

    // wait 10 seconds for connection:
    delay(10000);
  }
  server.begin();
  // you're connected now, so print out the status:
  printWifiStatus();

  // ----------------- SETUP FOR DHT22: ---------------------------
  Serial.println("DHT22 READING!!");
  dht.begin();

  // ----------------- SETUP FOR LIGHT SENSOR: ---------------------------
  Serial.println("Beginning Si1145!");

  while (!SI1145.Begin()) {
    Serial.println("Si1145 is not ready!");
    delay(1000);
  }
  Serial.println("Si1145 is ready!");
  Serial.print("//--------------------------------------//\r\n");
}

// ---------------------------------------------------------------------------------------------------------
// ---------------------------------------------------------------------------------------------------------
void loop() {

  // ----------------- LOOP FOR DHT22: ---------------------------
  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  // check if returns are valid, if they are NaN (not a number) then something went wrong!
  if (isnan(t) || isnan(h)) {
    Serial.println("Failed to read from DHT");
  } else {
    Serial.print("Humidity: "); 
    Serial.print(h);
    Serial.print(" %\t");
    Serial.print("Temperature: "); 
    Serial.print(t);
    Serial.println(" *C");
  }

  // ----------------- LOOP FOR SOIL MOISTURE SENSOR: -------------
  // read the value from the sensor:
  SMsensorValue = (analogRead(sensorPin) / moist_cal) * 100.00;
  Serial.print("Moisture = " );
  Serial.println(SMsensorValue);

  // ----------------- LOOP FOR LIGHT SENSOR: ---------------------
  Serial.print("Vis: "); Serial.println(SI1145.ReadVisible());
  Serial.print("IR: "); Serial.println(SI1145.ReadIR());
  //the real UV value must be div 100 from the reg value.
  Serial.print("UV: ");  Serial.println((float)SI1145.ReadUV()/100);
  
  // -------------OUTPUT TO NETWORK THOUG HTML AT MACHINE IP --------
  // TURNS THE WIFI LOW POWER MODE WHILE NO CLIENT
  WiFi.lowPowerMode();
  Serial.println("LowPowerMode ON");
  Serial.print("//--------------------------------------//\r\n");
  
  // listen for incoming clients
  WiFiClient client = server.available();
  if (client) {
    for (int i = 0; i < 50; i++) {            // blink for 5 seconds when server is avaliable
        digitalWrite(LED_BUILTIN, HIGH);    // turn the LED on (HIGH is the voltage level)
        delay(100);                         // wait for 0.1 second
        digitalWrite(LED_BUILTIN, LOW);     // turn the LED off by making the voltage LOW
        delay(100);                         // wait for 0.1 second  
    }
    Serial.println("new client");

    WiFi.noLowPowerMode();                // deactivate the wifi lowpower mode while client connected
    Serial.println("LowPowerMode OFF");
       
    // an http request ends with a blank line
    boolean currentLineIsBlank = true;
    while (client.connected()) {   
      
      if (client.available()) {        
        char c = client.read();
        Serial.write(c);
        // if you've gotten to the end of the line (received a newline
        // character) and the line is blank, the http request has ended,
        // so you can send a reply
        if (c == '\n' && currentLineIsBlank) {
          // send a standard http response header    
          client.println("HTTP/1.1 200 OK");
          client.println("Content-Type: application/json"); // Send a JSON format app in the header
          client.println("Connection: close");  // the connection will be closed after completion of the response
          client.println("Refresh: 60");  // refresh the page automatically every 1 minute
          client.println();
          //-----------------------JSON------------------------
          client.print("{");                                                                        // Initiate JSON string
          client.print("\"Temp\":\""); client.print(t); client.print("\",");                        // Temperature Value      
          client.print("\"Humid\":\""); client.print(h); client.print("\",");                       // Humidity Value         
          client.print("\"SoilM\":\""); client.print(SMsensorValue); client.print("\",");           // Soil Moisture Value
          client.print("\"Vis\":\""); client.print(SI1145.ReadVisible()); client.print("\",");      // Visible Light Value
          client.print("\"IR\":\""); client.print(SI1145.ReadIR()); client.print("\",");            // IR Light Value
          client.print("\"UV\":\""); client.print((float)SI1145.ReadUV()/100); client.print("\"");  // UV Light Value
          client.print("}");                                                                        // End JSON string   
          //-----------------------------------------------------    
          break;
        }
        if (c == '\n') {
          // you're starting a new line
          currentLineIsBlank = true;
        } else if (c != '\r') {
          // you've gotten a character on the current line
          currentLineIsBlank = false;
        }
      }
    }
    // give the web browser time to receive the data
    delay(1);

    // close the connection:
    client.stop();
    Serial.println("client disconnected");
  }
  
  delay(10000);     // Delay so reads occur once per second
}

//---------------------------------------------------------------------------

void printWifiStatus() {
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your board's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}
