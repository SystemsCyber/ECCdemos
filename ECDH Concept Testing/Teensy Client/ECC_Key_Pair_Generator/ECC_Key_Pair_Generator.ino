#include <uECC.h>

extern "C" {

int RNG(uint8_t *dest, unsigned size) {
  // Use the least-significant bits from the ADC for an unconnected pin (or connected to a source of 
  // random noise). This can take a long time to generate random data if the result of analogRead(0) 
  // doesn't change very frequently.
  while (size) {
    uint8_t val = 0;
    for (uint8_t i = 0; i < 8; ++i) {
      int init = analogRead(0);
      int count = 0;
      while (analogRead(0) == init) {
        ++count;
      }
      
      if (count == 0) {
         val = (val << 1) | (init & 0x01);
      } else {
         val = (val << 1) | (count & 0x01);
      }
    }
    *dest = val;
    ++dest;
    --size;
  }
  // NOTE: it would be a good idea to hash the resulting random data using SHA-256 or similar.
  return 1;
}

}  // extern "C"

#define num_bytes_secp160r1 20
#define num_bytes_secp192r1 24
#define num_bytes_secp224r1 28
#define num_bytes_secp256r1 32
#define num_bytes_secp256k1 32

char printable_byte[4];
  
void setup() {
  Serial.begin(115200);
  Serial.print("Generating ECC Key Pair\n");
  uECC_set_rng(&RNG);
}

void loop() {
  Serial.println("Selecting Curve");
  const struct uECC_Curve_t * curve = uECC_secp256r1();//Choose curve type
  const uint8_t curve_size = num_bytes_secp256r1;//Choose curve size
  const uint8_t secret_size = curve_size; // must be the same size as the curve.
  
  int private_key_size = uECC_curve_private_key_size(curve);
  Serial.print("Private key size: ");
  Serial.println(private_key_size);
  uint8_t private1[private_key_size];

  
  int public_key_size = uECC_curve_public_key_size(curve);
  Serial.print("Public key size: ");
  Serial.println(public_key_size);
  uint8_t public1[public_key_size];


  Serial.println("Making Key Pair 1");
  unsigned long a = millis();
  uECC_make_key(public1, private1, curve);
  unsigned long b = millis();
  Serial.print("Made key 1 in "); Serial.println(b-a);
  Serial.println("Public Key:");
  for (uint8_t i=0; i < public_key_size; i++){
    Serial.print("0X");
    if(public1[i]<16) Serial.print("0");
    Serial.print(public1[i],HEX);
    if(i<public_key_size-1) Serial.print(",");
  }
  Serial.println();
  Serial.println("Private Key:");
  for (uint8_t i=0; i < private_key_size; i++){
    Serial.print("0X");
    if(private1[i]<16) Serial.print("0");
    Serial.print(private1[i],HEX);
    if(i<private_key_size-1) Serial.print(",");
  }
  Serial.println();
  Serial.println();
  delay(5000);
 
}
