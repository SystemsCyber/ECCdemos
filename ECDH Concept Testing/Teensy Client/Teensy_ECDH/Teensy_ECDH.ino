#include <uECC.h>

#define num_bytes_secp160r1 20
#define num_bytes_secp192r1 24
#define num_bytes_secp224r1 28
#define num_bytes_secp256r1 32

char printable_byte[4];

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.print("Testing ECDH Concept\n");


  Serial.println("Selecting Curve");
  const struct uECC_Curve_t * curve = uECC_secp256r1();
  const uint8_t curve_size = num_bytes_secp256r1;
  const uint8_t secret_size = curve_size; // must be the same size as the curve.

  //Teensy private key and public key will be manually loaded here:
  int private_key_size = uECC_curve_private_key_size(curve);
  Serial.print("Private key size: ");
  Serial.println(private_key_size);
  uint8_t private1[private_key_size] = {0XB8,0X7E,0XC3,0X7C,0X04,0X4A,0X31,0XDB,0X47,0X32,0X77,0X19,0XBC,0XCA,0XEC,0X5D,0XE3,0X1F,0X09,0XE3,0X8F,0X2E,0XAA,0X11,0X1E,0XFA,0X7E,0X6C,0XAD,0X79,0X34,0XB2
};
    
  int public_key_size = uECC_curve_public_key_size(curve);
  Serial.print("Public key size: ");
  Serial.println(public_key_size);
  uint8_t public1[public_key_size]={0X93,0XFF,0X03,0XE1,0X6D,0XC0,0X95,0X72,0XAE,0XB7,0X00,0XDF,0XD0,0X07,0XFD,0X41,0X6D,0XC6,0XC8,0XD7,0X3E,0X6E,0X44,0X7A,0X6F,0X4C,0X9B,0XB8,0XF2,0X61,0X6A,0X40,0X14,0X58,0X95,0X93,0X1F,0X88,0XF6,0X82,0X08,0X09,0X0B,0X66,0X41,0X12,0XBE,0XC0,0XD0,0X5D,0XBF,0X2C,0X04,0XDC,0XFA,0XF6,0X39,0XAE,0XDE,0X70,0XB2,0XF3,0X89,0X0B
};

  //Server public key will be manually loaded here:
  uint8_t public2[public_key_size] = {0X43,0X2a,0X1e,0X88,0X18,0X3f,0Xed,0X09,0Xf7,0X39,0X97,0X1d,0X4a,0Xd0,0X73,0X5b,0Xb1,0X48,0X6c,0X7c,0X5c,0Xc4,0X6c,0Xf2,0Xe5,0X2d,0X05,0X6b,0X33,0Xa4,0X42,0X20,0X73,0X9a,0X7f,0X8f,0Xc1,0Xbb,0X3f,0X1e,0Xb4,0X88,0Xd4,0Xc9,0X55,0X59,0Xdc,0Xe1,0X15,0X20,0X17,0Xe9,0X44,0X2f,0X60,0X7b,0Xe9,0X35,0X5a,0X06,0Xcb,0X64,0X5f,0X18};

  
 //Print out Server Public Key
  Serial.println("Server Public Key:");
  for (uint8_t i=0; i < public_key_size; i++){
    sprintf(printable_byte,"%02X",public2[i]);
    Serial.print(printable_byte);
  }
  Serial.println();

 //Print out Teensy Private Key
  Serial.println("Teensy Private Key:");
  for (uint8_t i=0; i < private_key_size; i++){
    sprintf(printable_byte,"%02X",private1[i]);
    Serial.print(printable_byte);
  }
  
 //Print out Teensy Public Key
  Serial.println();
    Serial.println("Teensy Public Key:");
  for (uint8_t i=0; i < public_key_size; i++){
    Serial.print("0X");
    if(public1[i]<16)Serial.print("0");
    Serial.print(public1[i],HEX);
    if(i<public_key_size-1) Serial.print(",");
  }
  Serial.println();
  

  //Calculate shared secret from Server Public Key and Teensy Private Key:
  uint8_t secret1[secret_size];
  Serial.println("Calculating shared secret from Server Public Key.");
  unsigned long a = millis();
  int r = uECC_shared_secret(public2, private1, secret1, curve);
  unsigned long b = millis();
  Serial.print("Calculated shared secret in "); Serial.println(b-a);
  if (!r) {
    Serial.print("shared_secret() failed (1)\n");
    return;
  }
  Serial.println("Shared secret:");
  for (uint8_t i=0; i < secret_size; i++){
    sprintf(printable_byte,"%02X",secret1[i]);
    Serial.print(printable_byte);
  }
  Serial.println();
}
 
void loop() {
  
}
