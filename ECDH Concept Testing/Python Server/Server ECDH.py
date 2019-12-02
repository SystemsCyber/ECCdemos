from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import serialization
import base64
import struct

#generate server ECC key pair
server_private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
server_public_key = server_private_key.public_key()

#Serializing the server public key
serialized_public = server_public_key.public_bytes(
	encoding=serialization.Encoding.X962, #PEM
	format=serialization.PublicFormat.UncompressedPoint) #SubjectPublicKeyInfo)
print(serialized_public[1:])

#Serializing the server public key
serialized_public = server_public_key.public_bytes(
	encoding=serialization.Encoding.PEM,
	format=serialization.PublicFormat.SubjectPublicKeyInfo)

public_key_hex = ((base64.b64decode(serialized_public.splitlines()[1]).hex()) + \
					(base64.b64decode(serialized_public.splitlines()[2]).hex()))[54:]
public_key = b''
for i in range(0,len(public_key_hex),2):
	public_key += struct.pack("B",int(public_key_hex[i:i+2],16))
print(public_key)

public_key_1 = public_key_hex[0:64]
public_key_2 = public_key_hex[64:128]

public_key_list = []
for k in range(64):
	public_key_list.append('0X'+public_key_hex[2*k]+public_key_hex[2*k+1])

print("Server public Key is:",",".join(public_key_list),'\n')


PEM_public_key_first = '-----BEGIN PUBLIC KEY-----\nMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE'
PEM_public_key_last = '\n-----END PUBLIC KEY-----\n'
#Input Teensy public key manually here:
Teeny_public_key_hex = [0X93,0XFF,0X03,0XE1,0X6D,0XC0,0X95,0X72,0XAE,0XB7,0X00,0XDF,0XD0,0X07,0XFD,0X41,0X6D,0XC6,0XC8,0XD7,0X3E,0X6E,0X44,0X7A,0X6F,0X4C,0X9B,0XB8,0XF2,0X61,0X6A,0X40,0X14,0X58,0X95,0X93,0X1F,0X88,0XF6,0X82,0X08,0X09,0X0B,0X66,0X41,0X12,0XBE,0XC0,0XD0,0X5D,0XBF,0X2C,0X04,0XDC,0XFA,0XF6,0X39,0XAE,0XDE,0X70,0XB2,0XF3,0X89,0X0B]

#Convert Teensy public key to base64 format
Teensy_PEM_public_key = base64.b64encode(bytes(Teeny_public_key_hex)).decode('ascii')

#Finalize the teensy public key in serilized PEM format
public_key_teensy_string = PEM_public_key_first + Teensy_PEM_public_key[:28]+'\n'+ Teensy_PEM_public_key[28:] + PEM_public_key_last
serialized_public_teensy = bytes(public_key_teensy_string,'ascii')

#Print Teensy public key
public_key_hex_teensy = ((base64.b64decode(serialized_public_teensy.splitlines()[1]).hex()) + \
					(base64.b64decode(serialized_public_teensy.splitlines()[2]).hex()))[54:]
print("Teensy Public Key:",public_key_hex_teensy,"Length:", int(len(public_key_hex_teensy)/2),'\n')

#Load teensy public key
teensy_public_key = serialization.load_pem_public_key(serialized_public_teensy,backend=default_backend())

#Derive shared secret
shared_secret = server_private_key.exchange(ec.ECDH(),teensy_public_key)
print("Shared secret:",shared_secret.hex())

