# ECCdemos
Code snippets used to demonstrate how to use Elliptic Curve Cryptography in systems

## ECDH Concept Testing
This demo shows the concept of ECDH key exchange by showing the shared secret result from the Server (Python) and the Client (Teensy)

The first step is to generate an ECC key pair for the Client using the ECC_Key_Pair_Generator.ino script. The client public key will be manuanlly loaded into the Server ECDH.py script, where the server will generate an ECC key pair for itself and use its private key and the input client public key to calculate a shared secret. 

The server public key along with the client key pair generated before will be then manually loaded into the Teensy_ECDH.ino where the client will use its private key and the server public key to calculate a shared secret.

The shared secret will be the same for the client and the server, which demonstrates the Deffie-Hellman key exchange concept where public keys are exchanged, and the client and the server can use the other's public key to generate a same shared secret for further communication.
