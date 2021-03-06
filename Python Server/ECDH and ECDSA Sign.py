import base64
import json
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

print("ECDH----------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------------")
#generate server ECC key pair
server_private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
server_public_key = (server_private_key.public_key())

server_pem_key = server_private_key.private_bytes(
                        encoding = serialization.Encoding.PEM,
                        format = serialization.PrivateFormat.PKCS8,
                        encryption_algorithm = serialization.NoEncryption())
print(server_pem_key.decode('utf-8'))

server_public_key = server_private_key.public_key()
server_public_key_bytes = server_public_key.public_bytes(
    encoding = serialization.Encoding.X962,
    format = serialization.PublicFormat.UncompressedPoint)
print('server_public_key_bytes')
print(server_public_key_bytes.hex().upper())
print(len(server_public_key_bytes[1:]))

stored_key = base64.b64encode(server_public_key_bytes)
print(stored_key)
# load the device's public key which was a string representation of the key
device_bytes = base64.b64decode(stored_key)
device_public_key = ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(),device_bytes)

#Serializing the server public key
serialized_public = server_public_key.public_bytes(
	encoding=serialization.Encoding.PEM,
	format=serialization.PublicFormat.SubjectPublicKeyInfo)

#Convert server public key to base64 format
public_key_hex = ((base64.b64decode(serialized_public.splitlines()[1]).hex()) + \
					(base64.b64decode(serialized_public.splitlines()[2]).hex()))[54:]

public_key_1 = public_key_hex[0:64]
public_key_2 = public_key_hex[64:128]
#print(public_key_hex)
#print(public_key_1)
#print(public_key_2)
public_key_list = []
for k in range(64):

public_key_list.append('0x'+public_key_hex[2*k]+public_key_hex[2*k+1])

print("Server public Key is:")
for i, elem in enumerate(public_key_list):
    print(elem,end=' ')
    if i % 16 == 15:
        print("")
print("")


PEM_public_key_first = '-----BEGIN PUBLIC KEY-----\nMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE'
PEM_public_key_last = '\n-----END PUBLIC KEY-----\n'
#Input Teensy public key manually here:
Teeny_public_key_hex = [
0x0D, 0x5E, 0xDD, 0xA4, 0x80, 0x87, 0xFC, 0xF5, 0x11, 0xDF, 0x17, 0x56, 0x24, 0xD8, 0x55, 0xF6,
0x3A, 0xB9, 0x38, 0x98, 0x8E, 0x8A, 0xD7, 0x72, 0x24, 0xE1, 0x84, 0x67, 0x9B, 0xEB, 0x18, 0x48, 
0x8C, 0xC2, 0xE2, 0x00, 0xFF, 0x13, 0x1E, 0xA2, 0x43, 0xA1, 0x55, 0x26, 0xA1, 0xAC, 0xF2, 0x9F, 
0x78, 0x87, 0x24, 0xED, 0x73, 0x24, 0xC9, 0x9C, 0x38, 0x21, 0xB4, 0xE9, 0x2F, 0xA1, 0x0F, 0x78
]

#Convert Teensy public key to base64 format
Teensy_PEM_public_key = base64.b64encode(bytes(Teeny_public_key_hex)).decode('ascii')

#Finalize the teensy public key in serilized PEM format
public_key_teensy_string = PEM_public_key_first + Teensy_PEM_public_key[:28]+'\n'+ Teensy_PEM_public_key[28:] + PEM_public_key_last
serialized_public_teensy = bytes(public_key_teensy_string,'ascii')

#Print Teensy public key
public_key_hex_teensy = ((base64.b64decode(serialized_public_teensy.splitlines()[1]).hex()) + \
					(base64.b64decode(serialized_public_teensy.splitlines()[2]).hex()))[54:]
print("Teensy Public Key:",public_key_hex_teensy)
print("Length:", int(len(public_key_hex_teensy)/2))
print("")

#Load teensy public key
teensy_public_key = serialization.load_pem_public_key(serialized_public_teensy,backend=default_backend())

#Derive shared secret
shared_secret = server_private_key.exchange(ec.ECDH(),teensy_public_key)
print("Shared secret:",shared_secret.hex())
print(len(shared_secret))

session_key = base64.b64decode("7lv9V/0qYzgKdCZJOo3YFQ==")
print("encrypted Key: {}".format(session_key))
print(len(session_key))
cipher = Cipher(algorithms.AES(shared_secret), modes.ECB(), backend=default_backend())
decryptor = cipher.decryptor()
clear_key = decryptor.update(session_key) + decryptor.finalize()
print("Clear Key: {}".format(clear_key))
print(len(clear_key))
print("Clear Key JSON: {}".format(json.dumps(base64.b64encode(clear_key).decode('ascii'))))


print("")
print("Signing Data--------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------------")
#data to be signed
data_hex = [
0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F
]
data = bytes(data_hex)


signature1 = server_private_key.sign(data,ec.ECDSA(hashes.SHA256()))
signature1_hex = utils.decode_dss_signature(signature1)
#print(hex(signature1_hex[0]))
#print(hex(signature1_hex[1]))
string1 = hex(signature1_hex[0])[2:]
string2 = hex(signature1_hex[1])[2:]
int_list1=[]
int_list2=[]
for i in range(0,len(string2),2):
	int_list1.append(int(string1[i:i+2],16))
	int_list2.append(int(string2[i:i+2],16))
#print(int_list1)
#print(int_list1)
pretty_print_1 = " ".join(["0x{:02X}".format(b) for b in int_list1])
pretty_print_2 = " ".join(["0x{:02X}".format(b) for b in int_list2])
print("First 32 Bytes of Signature: ")
print(pretty_print_1)
print("Second 32 Bytes of Signature: ")
print(pretty_print_2)