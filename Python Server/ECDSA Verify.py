from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives import serialization
import base64
chosen_hash = hashes.SHA256()

PEM_public_key_first = '-----BEGIN PUBLIC KEY-----\nMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE'
PEM_public_key_last = '\n-----END PUBLIC KEY-----\n'

public_key_hex = [0x76, 0xE2, 0x92, 0x5C, 0xC1, 0xB1, 0xC5, 0x47, 0x20, 0x20, 0xB8, 0xCE, 0x84, 0xDD, 0x27, 0xE4, 
0xE1, 0x0A, 0x85, 0x21, 0x46, 0x29, 0x17, 0x03, 0x64, 0x74, 0x8A, 0x2D, 0x78, 0x6A, 0xDC, 0x4C, 
0xF8, 0x80, 0xAD, 0x60, 0x51, 0xFF, 0xFD, 0xBF, 0x7F, 0xEB, 0xEC, 0x94, 0x41, 0x95, 0xAD, 0xFA, 
0x46, 0x7A, 0xDA, 0x62, 0xEA, 0x7B, 0x84, 0x1D, 0xCB, 0x92, 0x64, 0xB6, 0x4D, 0x9A, 0x6D, 0xBE]

data_hex = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 
0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F]

signature_hex = [0x98, 0x07, 0x9F, 0xE1, 0x09, 0x01, 0x0C, 0x32, 0xFD, 0x84, 0xC2, 0x59, 0xF4, 0xD0, 0xEA, 0x86, 
0xB8, 0xAB, 0xE5, 0x85, 0x35, 0x2F, 0xBA, 0x85, 0x0C, 0xE4, 0x3A, 0xF6, 0x91, 0x3C, 0x19, 0xA4,
0x4A, 0xD7, 0xD0, 0x2A, 0x19, 0x50, 0x8F, 0x96, 0x41, 0xC3, 0xF7, 0x25, 0x87, 0x98, 0x6C, 0x8F, 
0x6B, 0x3A, 0xCE, 0x71, 0x15, 0x27, 0x6E, 0x79, 0x06, 0xB8, 0x5B, 0xCC, 0x76, 0xDB, 0x94, 0xBC, ]

publicKey = [
0x76, 0xE2, 0x92, 0x5C, 0xC1, 0xB1, 0xC5, 0x47, 0x20, 0x20, 0xB8, 0xCE, 0x84, 0xDD, 0x27, 0xE4, 
0xE1, 0x0A, 0x85, 0x21, 0x46, 0x29, 0x17, 0x03, 0x64, 0x74, 0x8A, 0x2D, 0x78, 0x6A, 0xDC, 0x4C, 
0xF8, 0x80, 0xAD, 0x60, 0x51, 0xFF, 0xFD, 0xBF, 0x7F, 0xEB, 0xEC, 0x94, 0x41, 0x95, 0xAD, 0xFA, 
0x46, 0x7A, 0xDA, 0x62, 0xEA, 0x7B, 0x84, 0x1D, 0xCB, 0x92, 0x64, 0xB6, 0x4D, 0x9A, 0x6D, 0xBE
];

signature = [
0x98, 0x07, 0x9F, 0xE1, 0x09, 0x01, 0x0C, 0x32, 0xFD, 0x84, 0xC2, 0x59, 0xF4, 0xD0, 0xEA, 0x86, 
0xB8, 0xAB, 0xE5, 0x85, 0x35, 0x2F, 0xBA, 0x85, 0x0C, 0xE4, 0x3A, 0xF6, 0x91, 0x3C, 0x19, 0xA4,
0x4A, 0xD7, 0xD0, 0x2A, 0x19, 0x50, 0x8F, 0x96, 0x41, 0xC3, 0xF7, 0x25, 0x87, 0x98, 0x6C, 0x8F, 
0x6B, 0x3A, 0xCE, 0x71, 0x15, 0x27, 0x6E, 0x79, 0x06, 0xB8, 0x5B, 0xCC, 0x76, 0xDB, 0x94, 0xBC 
];


data = bytes(data_hex)
print("Data is:", data)
print("")
#Load Public Key
PEM_public_key = base64.b64encode(bytes(public_key_hex)).decode('ascii')
public_key_string = PEM_public_key_first + PEM_public_key[:28]+'\n'+ PEM_public_key[28:] + PEM_public_key_last
serialized_public_teensy = bytes(public_key_string,'ascii')
public_key = serialization.load_pem_public_key(serialized_public_teensy,backend=default_backend())

#Convert Signature to DER format
signature_r = 0
signature_s = 0
for i in range(32):
	signature_r = signature_r<<8|signature_hex[i]
	signature_s = signature_s<<8|signature_hex[i+32]
#print(hex(signature_r))
#print(hex(signature_s))
signature = utils.encode_dss_signature(signature_r,signature_s)
print("Signature is:",signature)
print("")

#Verify the signature
if public_key.verify(signature,data,ec.ECDSA(utils.Prehashed(chosen_hash))) == None:
	print("Verify Signature Successfully!")


