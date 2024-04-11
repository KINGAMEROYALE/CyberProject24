import datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from datetime import *

pub_key_path = 'C:\\Users\\ניר\\cyberproject24\\pub_key'
priv_key_path = 'C:\\Users\\ניר\\cyberproject24\\priv_key'

def init_once():
    key = RSA.generate(2048)
    private_key = key.export_key('PEM')
    f = open (pub_key_path,"wb")
    public_key = f.write(private_key)
    f.close()
    f = open (priv_key_path,"wb")
    public_key = f.write(private_key)
    f.close()
    public_key = key.publickey().exportKey('PEM')
   
def rsa_encrypt_msg(message):
    message = str.encode(message)
    f = open (pub_key_path,"rb")
    public_key = f.read()
    f.close()
    rsa_public_key = RSA.importKey(public_key)
    rsa_public_key = PKCS1_OAEP.new(rsa_public_key)
    encrypted_text = rsa_public_key.encrypt(message)
    return encrypted_text

def rsa_decrypt_msg(encrypted_text):
    f = open (priv_key_path,"rb")
    private_key = f.read()
    f.close()
    rsa_private_key = RSA.importKey(private_key)
    rsa_private_key = PKCS1_OAEP.new(rsa_private_key)
    decrypted_text = rsa_private_key.decrypt(encrypted_text)
    return decrypted_text


def time_now():

    # Get the current date and time
    now = datetime.now()

    # Convert the date and time to an integer using the timestamp() method
    timestamp = int(now.timestamp())
    return timestamp

get_client_id_msg = "Please enter client ID:"
server_ip = "127.0.0.1"
server_port = 7999
successful_connection = "connection_established"