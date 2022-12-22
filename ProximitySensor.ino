/****************************************************************
  ProximitySensor.ino
  APDS-9930 ambient light and proximity sensor
  Davide Depau
  December 11, 2015
  https://github.com/Davideddu/APDS9930

  Shawn Hymel @ SparkFun Electronics
  October 28, 2014
  https://github.com/sparkfun/APDS-9960_RGB_and_Gesture_Sensor

  Tests the proximity sensing abilities of the APDS-9930.
  Configures the APDS-9930 over I2C and polls for the distance to
  the object nearest the sensor.

  Hardware Connections:

  IMPORTANT: The APDS-9930 can only accept 3.3V!

  Arduino Pin  APDS-9930 Board  Function

  3.3V         VCC              Power
  GND          GND              Ground
  A4           SDA              I2C Data
  A5           SCL              I2C Clock

  Resources:
  Include Wire.h and SparkFun_APDS-9930.h

  Development environment specifics:
  Written in Arduino 1.0.5
  Tested with SparkFun Arduino Pro Mini 3.3V

  This code is beerware; if you see me (or any other SparkFun
  employee) at the local, and you've found our code helpful, please
  buy us a round!

  Distributed as-is; no warranty is given.
****************************************************************/

#define DUMP_REGS

#include <Wire.h>
#include <APDS9930.h>

#include <WiFiNINA.h>

#include "arduino_wifipassword.h"

char ssid[] = SECRET_SSID;        // your network SSID (name)
char pass[] = SECRET_PASS;    // your network password (use for WPA, or use as key for WEP)
int status = WL_IDLE_STATUS;     // the Wifi radio's status

// Global Variables
APDS9930 apds = APDS9930();
uint16_t proximity_data = 0;

int val;

void setup() {

  //Initialize serial and wait for port to open:
  Serial.begin(9600);
  while (!Serial);

  // attempt to connect to Wifi network:
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to network: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network:
    status = WiFi.begin(ssid, pass);

    // wait 10 seconds for connection:
    delay(10000);
  }

  // you're connected now, so print out the data:
  Serial.println("You're connected to the network");

  Serial.println("----------------------------------------");
  printData();
  Serial.println("----------------------------------------");



  pinMode(11, INPUT);
  //analogReference(EXTERNAL);

  // Initialize Serial port
  Serial.begin(9600);
  Serial.println();
  Serial.println(F("---------------------------"));
  Serial.println(F("APDS-9930 - ProximitySensor"));
  Serial.println(F("---------------------------"));

  // Initialize APDS-9930 (configure I2C and initial values)
  if ( apds.init() ) {
    Serial.println(F("APDS-9930 initialization complete"));
  } else {
    Serial.println(F("Something went wrong during APDS-9930 init!"));
  }

  // // Adjust the Proximity sensor gain
  // if ( !apds.setProximityGain(PGAIN_2X) ) {
  //   Serial.println(F("Something went wrong trying to set PGAIN"));
  // }

  // Start running the APDS-9930 proximity sensor (no interrupts)
  if ( apds.enableProximitySensor(false) ) {
    Serial.println(F("Proximity sensor is now running"));
  } else {
    Serial.println(F("Something went wrong during sensor init!"));
  }


#ifdef DUMP_REGS
  /* Register dump */
  uint8_t reg;
  uint8_t val;

  for (reg = 0x00; reg <= 0x19; reg++) {
    if ( (reg != 0x10) && \
         (reg != 0x11) )
    {
      apds.wireReadDataByte(reg, val);
      Serial.print(reg, HEX);
      Serial.print(": 0x");
      Serial.println(val, HEX);
    }
  }
  apds.wireReadDataByte(0x1E, val);
  Serial.print(0x1E, HEX);
  Serial.print(": 0x");
  Serial.println(val, HEX);
#endif
}

void loop() {

    // Read the proximity value
  if ( !apds.readProximity(proximity_data) ) {
    Serial.println("Error reading proximity value");
  } else {
    Serial.print("Proximity: ");
    Serial.println(proximity_data);

  }
  if (proximity_data > 1000) {
    Serial.println("locked!");
  }
  else if (proximity_data <=800) {
    Serial.println("Unlocked");
  }

  val = digitalRead(11);

  if (val == HIGH) {
    Serial.println("Door closed");
  }
  else {
    Serial.println("Door Open");

  }
  // Wait 250 ms before next reading
  delay(2000);

    // check the network connection once every 10 seconds:
  //delay(250);
  //printData();
  //Serial.println("----------------------------------------");

}


  void printData() {
    Serial.println("Board Information:");
    // print your board's IP address:
    IPAddress ip = WiFi.localIP();
    Serial.print("IP Address: ");
    Serial.println(ip);

    Serial.println();
    Serial.println("Network Information:");
    Serial.print("SSID: ");
    Serial.println(WiFi.SSID());

    // print the received signal strength:
    long rssi = WiFi.RSSI();
    Serial.print("signal strength (RSSI):");
    Serial.println(rssi);

    byte encryption = WiFi.encryptionType();
    Serial.print("Encryption Type:");
    Serial.println(encryption, HEX);
    Serial.println();
  }
