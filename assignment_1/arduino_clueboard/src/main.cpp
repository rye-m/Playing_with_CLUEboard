// #include "Adafruit_Arcada.h"
// Adafruit_Arcada arcada;

#include <Adafruit_VCNL4040.h>

Adafruit_VCNL4040 vcnl4040 = Adafruit_VCNL4040();
unsigned long Time_marker_previous = 0;
unsigned long Time_marker = 0;
unsigned long interval = 99;
bool proximityTimeStored = false;

// Define pin assignments for the CLUE board
#define BUTTON_A_PIN 5  // Pin connected to button A
#define BUTTON_B_PIN 11 // Pin connected to button B
bool lastButtonAState = HIGH;
bool lastButtonBState = HIGH;
unsigned long lastDebounceTime = 0;
unsigned long debounceDelay = 50; // Debounce time in milliseconds

// internal readwrite
#include <Adafruit_LittleFS.h>
#include <InternalFileSystem.h>
#include <Adafruit_TinyUSB.h> // for Serial

using namespace Adafruit_LittleFS_Namespace;

#define FILENAME    "/adafruit.txt"
#define CONTENTS    "Adafruit Little File System test file contents"

File file(InternalFS);




void setup()
{
  Serial.begin(115200);
  // Wait until serial port is opened
  while (!Serial)
  {
    delay(1);
  }

  Serial.println("Adafruit VCNL4040 Config demo");

  if (!vcnl4040.begin())
  {
    Serial.println("Couldn't find VCNL4040 chip");
    while (1)
      ;
  }
  Serial.println("Found VCNL4040 chip");

  // vcnl4040.setProximityLEDCurrent(VCNL4040_LED_CURRENT_200MA);
  Serial.print("Proximity LED current set to: ");
  switch (vcnl4040.getProximityLEDCurrent())
  {
  case VCNL4040_LED_CURRENT_50MA:
    Serial.println("50 mA");
    break;
  case VCNL4040_LED_CURRENT_75MA:
    Serial.println("75 mA");
    break;
  case VCNL4040_LED_CURRENT_100MA:
    Serial.println("100 mA");
    break;
  case VCNL4040_LED_CURRENT_120MA:
    Serial.println("120 mA");
    break;
  case VCNL4040_LED_CURRENT_140MA:
    Serial.println("140 mA");
    break;
  case VCNL4040_LED_CURRENT_160MA:
    Serial.println("160 mA");
    break;
  case VCNL4040_LED_CURRENT_180MA:
    Serial.println("180 mA");
    break;
  case VCNL4040_LED_CURRENT_200MA:
    Serial.println("200 mA");
    break;
  }

  // vcnl4040.setProximityLEDDutyCycle(VCNL4040_LED_DUTY_1_40);
  Serial.print("Proximity LED duty cycle set to: ");
  switch (vcnl4040.getProximityLEDDutyCycle())
  {
  case VCNL4040_LED_DUTY_1_40:
    Serial.println("1/40");
    break;
  case VCNL4040_LED_DUTY_1_80:
    Serial.println("1/80");
    break;
  case VCNL4040_LED_DUTY_1_160:
    Serial.println("1/160");
    break;
  case VCNL4040_LED_DUTY_1_320:
    Serial.println("1/320");
    break;
  }

  // vcnl4040.setAmbientIntegrationTime(VCNL4040_AMBIENT_INTEGRATION_TIME_80MS);
  Serial.print("Ambient light integration time set to: ");
  switch (vcnl4040.getAmbientIntegrationTime())
  {
  case VCNL4040_AMBIENT_INTEGRATION_TIME_80MS:
    Serial.println("80 ms");
    break;
  case VCNL4040_AMBIENT_INTEGRATION_TIME_160MS:
    Serial.println("160 ms");
    break;
  case VCNL4040_AMBIENT_INTEGRATION_TIME_320MS:
    Serial.println("320 ms");
    break;
  case VCNL4040_AMBIENT_INTEGRATION_TIME_640MS:
    Serial.println("640 ms");
    break;
  }

  // vcnl4040.setProximityIntegrationTime(VCNL4040_PROXIMITY_INTEGRATION_TIME_8T);
  Serial.print("Proximity integration time set to: ");
  switch (vcnl4040.getProximityIntegrationTime())
  {
  case VCNL4040_PROXIMITY_INTEGRATION_TIME_1T:
    Serial.println("1T");
    break;
  case VCNL4040_PROXIMITY_INTEGRATION_TIME_1_5T:
    Serial.println("1.5T");
    break;
  case VCNL4040_PROXIMITY_INTEGRATION_TIME_2T:
    Serial.println("2T");
    break;
  case VCNL4040_PROXIMITY_INTEGRATION_TIME_2_5T:
    Serial.println("2.5T");
    break;
  case VCNL4040_PROXIMITY_INTEGRATION_TIME_3T:
    Serial.println("3T");
    break;
  case VCNL4040_PROXIMITY_INTEGRATION_TIME_3_5T:
    Serial.println("3.5T");
    break;
  case VCNL4040_PROXIMITY_INTEGRATION_TIME_4T:
    Serial.println("4T");
    break;
  case VCNL4040_PROXIMITY_INTEGRATION_TIME_8T:
    Serial.println("8T");
    break;
  }

  // vcnl4040.setProximityHighResolution(false);
  Serial.print("Proximity measurement high resolution? ");
  Serial.println(vcnl4040.getProximityHighResolution() ? "True" : "False");

  Serial.println("");

  pinMode(BUTTON_A_PIN, INPUT_PULLUP);
  pinMode(BUTTON_B_PIN, INPUT_PULLUP);

    // Initialize Internal File System
  InternalFS.begin();
}

void loop()
{

  bool buttonAState = digitalRead(BUTTON_A_PIN);

  // Check if button A was pressed (transition from HIGH to LOW)
  if (buttonAState == LOW && lastButtonAState == HIGH) {

    if ((millis() - lastDebounceTime) > debounceDelay) {
      lastDebounceTime = millis();

      while (true) {
        bool buttonBState = digitalRead(BUTTON_B_PIN);


        if (vcnl4040.getProximity() >= 50) {
          Time_marker = millis();
          interval = Time_marker - Time_marker_previous;

          if (interval > 21) {
            Serial.print("Proximity: "); Serial.print(vcnl4040.getProximity()); Serial.print("  ");
            Serial.print("Interval: "); Serial.println(interval);
          }
          Time_marker_previous = Time_marker;
        }

        delay(1);
        if (buttonBState == LOW) {
          Serial.println("break");
          file.open(FILENAME, FILE_O_READ);

        // file existed
        if ( file )
        {
          Serial.println(FILENAME " file exists");
          
          uint32_t readlen;
          char buffer[64] = { 0 };
          readlen = file.read(buffer, sizeof(buffer));

          buffer[readlen] = 0;
          Serial.println(buffer);
          file.close();
        }else
        {
          Serial.print("Open " FILENAME " file to write ... ");

          if( file.open(FILENAME, FILE_O_WRITE) )
          {
            Serial.println("OK");
            file.write(CONTENTS, strlen(CONTENTS));
            file.close();
          }else
          {
            Serial.println("Failed!");
          }
        }

        Serial.println("Internal ReadWrite Done");

          break;
        }
      }
    }}
  //  if (buttonBState == LOW && lastButtonBState == HIGH) {

  //    if ((millis() - lastDebounceTime) > debounceDelay) {
  //       lastDebounceTime = millis();
  //       Serial.println("hi");
  // }}
}