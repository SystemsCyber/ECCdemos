from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
#from cryptography.hazmat.primitives.kdf.hkdf import HKDF
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
# print(public_key_hex)
# for i in range(len(public_key_hex)):
#     print("0x"+public_key_hex[i:i+2],end=' ')
#     if i % 32 == 31:
#         print("")
