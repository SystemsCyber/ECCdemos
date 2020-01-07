/*
  Using the SparkFun Cryptographic Co-processor Breakout ATECC508a (Qwiic)
  By: Pete Lewis
  SparkFun Electronics
  Date: August 5th, 2019
  License: This code is public domain but you can buy me a beer if you use this and we meet someday (Beerware license).

  Feel like supporting our work? Please buy a board from SparkFun!
  https://www.sparkfun.com/products/15573

  This example shows how to create a digital signature (ECC type) on 32 bytes of data.
  Note, this requires that your device be configured with SparkFun Standard Configuration settings.
  By default, this example uses the private key securely stored and locked in slot 0.

  Hardware Connections and initial setup:
  Install artemis in boards manager: http://boardsmanager/All#Sparkfun_artemis
  Plug in your controller board (e.g. Artemis Redboard, Nano, ATP) into your computer with USB cable.
  Connect your Cryptographic Co-processor to your controller board via a qwiic cable.
  Select TOOLS>>BOARD>>"SparkFun Redboard Artemis"
  Select TOOLS>>PORT>> "COM 3" (note, yours may be different)
  Click upload, and follow configuration prompt on serial monitor at 115200.

*/

#include <SparkFun_ATECCX08a_Arduino_Library.h> //Click here to get the library: http://librarymanager/All#SparkFun_ATECCX08a
#include <i2c_t3.h>

ATECCX08A atecc;

uint8_t message[16] = {
  0xCB,0x39,0x44,0xD1,0x88,0x1F,0xB2,0xA0,0xAF,0xF3,0x50,0xD5,0x1F,0xB0,0xD8,0x02
};

uint8_t server_public_key[64] = {
0xAC,0x18,0xCF,0x17,0x3A,0x31,0x40,0x56,0x44,0x48,0x41,0xE4,0x52,0x2C,0x90,0xD5,0x1A,0xEA,0xEC,0x42,0xA7,0x14,0xBD,0x1B,0x4E,0x4E,0xEB,0x11,0x13,0xB9,0xF7,0xA1,0x15,0xEF,0x6B,0xC6,0xF1,0x32,0xB7,0xEC,0x12,0x19,0xD6,0x43,0x0C,0x24,0x0A,0xC4,0xE3,0xE0,0x65,0x23,0xD3,0xAE,0x09,0xB5,0xFD,0xE8,0x7D,0x9E,0x90,0x43,0xDC,0x33};


void setup() {
  while(!Serial);
  Wire.begin(I2C_MASTER, 0x00, I2C_PINS_18_19, I2C_PULLUP_EXT, 100000);
  Serial.begin(115200);
  if (atecc.begin() == true)
  {
    Serial.println("Successful wakeUp(). I2C connections are good.");
  }
  else
  {
    Serial.println("Device not found. Check wiring.");
    while (1); // stall out forever
  }

  printInfo(); // see function below for library calls and data handling

  // check for configuration
  if (!(atecc.configLockStatus))
  {
    Serial.print("Device not configured. Please use the configuration sketch.");
    while (1); // stall out forever.
  }

    Serial.print("Load Server Public Key: \t");
    if (atecc.loadPublicKey(server_public_key) == false) Serial.println("Failure.");

    Serial.print("Lock Data-OTP: \t");
    if (atecc.lockDataAndOTP() == true) Serial.println("Success!");
    else Serial.println("Failure.");

    Serial.print("Lock Slot 0: \t");
    if (atecc.lockDataSlot0() == true) Serial.println("Success!");
    else Serial.println("Failure.");
  atecc.readPublicKey(true);
  //Let's create a share secret and load in tempkey!
  atecc.ECDH(atecc.storedPublicKey, ECDH_OUTPUT_IN_TEMPKEY,0x0000);

  //Let's encrypt data
  atecc.AES_ECB(message);
}

void loop()
{
  // do nothing.
}



void printInfo()
{
  // Read all 128 bytes of Configuration Zone
  // These will be stored in an array within the instance named: atecc.configZone[128]
  atecc.readConfigZone(false); // Debug argument false (OFF)

  // Print useful information from configuration zone data
  Serial.println();

  Serial.print("Serial Number: \t");
  for (int i = 0 ; i < 9 ; i++)
  {
    if ((atecc.serialNumber[i] >> 4) == 0) Serial.print("0"); // print preceeding high nibble if it's zero
    Serial.print(atecc.serialNumber[i], HEX);
  }
  Serial.println();

  Serial.print("Rev Number: \t");
  for (int i = 0 ; i < 4 ; i++)
  {
    if ((atecc.revisionNumber[i] >> 4) == 0) Serial.print("0"); // print preceeding high nibble if it's zero
    Serial.print(atecc.revisionNumber[i], HEX);
  }
  Serial.println();

  Serial.print("Config Zone: \t");
  if (atecc.configLockStatus) Serial.println("Locked");
  else Serial.println("NOT Locked");

  Serial.print("Data/OTP Zone: \t");
  if (atecc.dataOTPLockStatus) Serial.println("Locked");
  else Serial.println("NOT Locked");

  Serial.print("Data Slot 0: \t");
  if (atecc.slot0LockStatus) Serial.println("Locked");
  else Serial.println("NOT Locked");

  Serial.println();

  // if everything is locked up, then configuration is complete, so let's print the public key
  if (atecc.configLockStatus) 
  {
    if(atecc.generatePublicKey(0x0000) == false)
    {
      Serial.println("Failure to generate this device's Public Key");
      Serial.println();
    }
  }
}
